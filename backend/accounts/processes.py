import logging
from django.utils import timezone
from apps.accounts.models import profile, activation_data
from backend.common.processes import BaseHandler, africastalkingResponseHandler, record_user_activity
from backend.common.send_sms import SendSMSHandler
from apps.common.models import sentSMSLogs, userActivities
from .tokens import account_activation_token
from django.contrib.auth.models import User

logging = logging.getLogger('accounts_backend')


class RegistrationHandler:
    @staticmethod
    def register_user_api(user, mobile_number, username):
        try:
            user.is_active = False
            user.save()
            user = User.objects.get(username=username)
            RegistrationHandler.register_profile(user, mobile_number)
            return True
        except Exception as e:
            logging.info(e)
            raise e

    @staticmethod
    def register_user(user, mobile_number):
        try:
            user.is_active = False
            user.save()
            RegistrationHandler.register_profile(user, mobile_number)
            return True
        except Exception as e:
            logging.info(e)
            raise e

    @staticmethod
    def register_profile(user, mobile_number):
        try:
            data = profile()
            data.username_id = user.id
            data.mobile_number = mobile_number
            data.operator = BaseHandler.telco_operator_finder(mobile_number)
            data.slug = mobile_number
            data.date = timezone.now
            data.save()
            RegistrationHandler.register_activation_details(user, mobile_number, sentSMSLogs.REG)
            record_user_activity(userActivities.USER_REGISTRATION, mobile_number,
                                                 userActivities.COMPLETED)
            return True
        except Exception as e:
            logging.info(e)
            raise e

    @staticmethod
    def register_activation_details(user, mobile_number, category):
        try:
            min_char = 6
            max_char = 6
            code = BaseHandler.get_verify_code(min_char, max_char)
            token = account_activation_token.make_token(user)
            act = activation_data()
            try:
                tk = activation_data.objects.filter(token=token)
            except(TypeError, ValueError, OverflowError, activation_data.DoesNotExist):
                tk = None
            if tk is not None:
                activation_data.objects.filter(token=token).delete()
                act.username = user.username
                act.code = code
                act.token = token
                act.mobile_number = mobile_number
                act.status = "unverified"
                act.date = timezone.now
                act.save()
            else:
                act.username = user.username
                act.code = code
                act.token = token
                act.mobile_number = mobile_number
                act.status = "unverified"
                act.date = timezone.now
                act.save()
            logging.info(" Your Phone is: {0}".format(str(mobile_number)))
            logging.info(" Your activation token is: {0}".format(str(token)))
            logging.info(" Your activation code is: {0}".format(str(code)))
            message = "Your Genus verification code is: {0}".format(code)
            logging.info(message)
            response = SendSMSHandler.africaStalkingSMS(mobile_number, message)
            africastalkingResponseHandler.record_africastalking_sms_response(response, category, mobile_number)
            BaseHandler.sent_sms_logs(mobile_number, message, category)
            # This is to be sent for email verification if email address applies
            # http://127.0.0.1:8000/a/activate/MTQ/506-07bac31c7df7ee8818bc/
            return True
        except Exception as e:
            logging.info(e)
            raise e

    @staticmethod
    def sms_code_activation(mobile_number, code):
        try:
            logging.info("{0}".format(str("Data was found")))
            data = activation_data.objects.get(code=code, mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, activation_data.DoesNotExist):
            logging.info("Data was not found")
            data = None
        if data is not None:
            if data.status == "verified":
                logging.info(
                    "This code: {0} has been provided for this user: {1} but it has been verified already.".format(
                        str(code), str(mobile_number)))
                logging.info("The code provided is invalid!")
                return "error0"
            else:
                user = User.objects.get(username=data.username)
                if user is not None and account_activation_token.check_token(user, data.token):
                    user.is_active = True
                    user.save()
                    activation_data.objects.filter(code=code, mobile_number=mobile_number).update(status="verified")
                    return user
                else:
                    logging.info(ValueError("Invalid verification token used."))
                    return "error1"
        else:
            logging.info(ValueError("Invalid code and phone number provided"))
            return "error2"


class PassResetHandler:
    @staticmethod
    def process_reset_code(mobile_number):
        try:
            logging.info("Ready to process reset code")
            data = profile.objects.get(mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
            logging.info("Phone number was not found")
            data = None
        if data is not None:
            try:
                user = User.objects.get(pk=data.username_id)
                RegistrationHandler.register_activation_details(user, mobile_number, sentSMSLogs.RESET_PASSWORD_REQUEST)
                return True
            except Exception as e:
                logging.exception(e)
                return False

    @staticmethod
    def set_new_password(mobile_number, new_password):
        try:
            data = profile.objects.get(mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
            logging.info("Phone number was not found")
            data = None
        if data is not None:
            try:
                u = User.objects.get(pk=data.username_id)
                u.set_password(new_password)
                u.save()
                record_user_activity(userActivities.RESET_PASSWORD, mobile_number,
                                     userActivities.COMPLETED)
                return True
            except Exception as e:
                logging.exception(e)
                return False
