import logging, json, string
from random import choice, randint
from django.utils import timezone
from decouple import config
from apps.accounts.models import profile, activation_data
from apps.common.models import sentSMSLogs, userActivities
from apps.sms.models import africasTalkingResponses, AfrikaStalkingSMSMetrics
from django.contrib.auth.models import User


logging = logging.getLogger('common_backend')


class BaseHandler:
    @staticmethod
    def mobile_number_exists(mobile_number):
        try:
            mobile = profile.objects.get(mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
            mobile = None
        if mobile is not None:
            logging.info("Mobile number: {0} exists".format(str(mobile_number)))
            return True
        else:
            logging.info("Mobile number: {0} does not exist".format(str(mobile_number)))
            return False

    @staticmethod
    def get_verify_code(min_char, max_char):
        try:
            code = None
            counter = True
            while counter is True:
                r = TKVr(min_char, max_char)
                code = r.verify_ld_code_generator()
                if code is not None:
                    counter = BaseHandler.verify_code_exists(code)
                else:
                    raise ValueError("Code generation failed")
            return code
        except Exception as e:
            logging.info(e)
            raise e

    @staticmethod
    def verify_code_exists(code):
        try:
            Code_ = activation_data.objects.get(code=code)
        except(TypeError, ValueError, OverflowError, activation_data.DoesNotExist):
            Code_ = None
        if Code_ is not None:
            logging.info("Code: {0} is invalid.".format(code))
            return True
        else:
            logging.info("Code: {0} is valid.".format(code))
            return False

    @staticmethod
    def telco_operator_finder(mobile_number):
        try:
            if mobile_number.startswith("+"):
                mobile_number = mobile_number[1:]
            elif mobile_number.startswith("0"):
                mobile_number = "254" + mobile_number[1:]
            else:
                mobile_number = mobile_number
            with open(config("PREFIXES_PATH")) as json_data:
                data = json.load(json_data)
            prefix = mobile_number[:5]
            logging.info(prefix)
            return data["prefix"][prefix][1]
        except Exception as e:
            logging.exception(e)
            return "unknown"

    @staticmethod
    def sent_sms_logs(mobile_number, message, category):
        try:
            user = profile.objects.get(mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
            user = None
        if user is None:
            logging.warning(
                "Attempted to save sent SMS log to mobile number {0} which is not registered".format(
                    str(mobile_number)))
            return False
        else:
            try:
                user = User.objects.get(pk=user.username_id)
                sms_log = sentSMSLogs(username=user.username, mobile_number=mobile_number, message_sent=message,
                                      category=category)
                sms_log.save()
                logging.info("Saved sent sms log for user {0}".format(str(mobile_number)))
                return True
            except Exception as e:
                logging.error("Failed to save sent sms log for user {0}".format(str(mobile_number)))
                logging.exception(e)
                return False


class ActivityHandler:

    @staticmethod
    def update_user_activity(action, user, code):
        pass
        return True


def record_user_activity(action, mobile_number, status):
    try:
        user = profile.objects.get(mobile_number=mobile_number)
    except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
        user = None
    if user is None:
        logging.warning(
            "Attempting to save activity but user is not registered with phone number".format(
                str(mobile_number)))
        return False
    else:
        code = BaseHandler.get_verify_code(7, 7)
        user = User.objects.get(pk=user.username_id)
        try:
            data = userActivities()
            data.username = user.username
            data.mobile_number = mobile_number
            data.action = action
            data.token = code
            data.status = status
            data.created_on = timezone.now
            data.state_changed_on = timezone.now
            data.slug = code
            data.save()
            context = {
                'status': True,
                'code': code,
            }
            return context
        except Exception as e:
            logging.error("Failed to save activity for user with mobile number: {0}".format(
                str(mobile_number)))
            logging.info(e)
            context = {
                'status': False,
                'code': None,
            }
            return context


class TKVr:
    def __init__(self, min_char, max_char):
        self.min_char = min_char
        self.max_char = max_char
        self.lpd = string.ascii_letters + string.punctuation + string.digits
        self.lp = string.ascii_letters + string.punctuation
        self.ld = string.ascii_letters + string.digits
        self.pd = string.punctuation + string.digits

    def verify_lpd_code_generator(self):
        code = "".join(choice(self.lpd) for x in range(randint(self.min_char, self.max_char)))
        logging.info("This is your verification code : {0}".format(str(code)))
        return code

    def verify_lp_code_generator(self):
        code = "".join(choice(self.lp) for x in range(randint(self.min_char, self.max_char)))
        logging.info("This is your verification code : {0}".format(str(code)))
        return code

    def verify_ld_code_generator(self):
        code = "".join(choice(self.ld) for x in range(randint(self.min_char, self.max_char)))
        logging.info("This is your verification code : {0}".format(str(code)))
        return code

    def verify_pd_code_generator(self):
        code = "".join(choice(self.pd) for x in range(randint(self.min_char, self.max_char)))
        logging.info("This is your verification code : {0}".format(str(code)))
        return code


class africastalkingResponseHandler:
    @staticmethod
    def record_africastalking_sms_response(response, category, mobile_number):
        try:
            user = profile.objects.get(mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
            user = None
        if user is None:
            logging.warning(
                "Attempted to save Africa's Talking sent sms response but user with mobile number {0} does not exist.".format(
                    str(mobile_number)))
            return False
        else:
            try:
                if response['SMSMessageData']['Recipients'][0]['status'] == "Success":
                    user = User.objects.get(pk=user.username_id)
                    data = africasTalkingResponses()
                    data.username = user.username
                    data.mobile_number = mobile_number
                    data.sms_target = category
                    data.response_message = response['SMSMessageData']['Message']
                    data.status = response['SMSMessageData']['Recipients'][0]['status']
                    data.statusCode = response['SMSMessageData']['Recipients'][0]['statusCode']
                    data.cost = response['SMSMessageData']['Recipients'][0]['cost']
                    data.number = response['SMSMessageData']['Recipients'][0]['number']
                    data.messageId = response['SMSMessageData']['Recipients'][0]['messageId']
                    data.save()
                    AfricaStalkingMetricsHandler.update_metrics(category,
                                                                response['SMSMessageData']['Recipients'][0]['cost'])
                    logging.info("Saved Africa's Talking response body {0}".format(str(mobile_number)))
                    return True
                else:
                    logging.info(
                        "Received unsuccessful response from Africa's Talking when trying to send sms to user".format(
                            str(mobile_number)))
                    return False
            except Exception as e:
                logging.error("Failed to save Africa's Talking sms response body for user: {0}".format(
                    str(mobile_number)))
                logging.exception(e)
                return False


class AfricaStalkingMetricsHandler:
    @staticmethod
    def update_metrics(target, cost):
        try:
            metric = AfrikaStalkingSMSMetrics.objects.get(sms_target=target)
        except(TypeError, ValueError, OverflowError, AfrikaStalkingSMSMetrics.DoesNotExist):
            metric = None
        if metric is None:
            logging.warning(
                "Failed to save metrics for africastalking metrics for sms category : {0}".format(str(target)))
            return False
        else:
            total_sms = metric.total_sent + 1
            amnt = cost.split(' ')
            total_cost = metric.total_cost + float(amnt[1])
            try:
                d = AfrikaStalkingSMSMetrics.objects.get(sms_target=target)
                d.total_sent = int(total_sms)
                d.total_cost = float(total_cost)
                d.save()
                return True
            except Exception as e:
                logging.info(e)
                return False
