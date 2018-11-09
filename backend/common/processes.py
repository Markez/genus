import logging, json, string
from random import choice, randint
from decouple import config
from apps.accounts.models import profile, activation_data
from apps.common.models import sentSMSLogs
from django.contrib.auth.models import User


logging = logging.getLogger('common_backend')


class BaseHandler:
    @staticmethod
    def mobileNumberExists(mobile_number):
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
    def getVerifyCode(min_char, max_char):
        try:
            code = None
            counter = True
            while counter is True:
                code = BaseHandler.verifyCodeGenerator(min_char, max_char)
                if code is not None:
                    counter = BaseHandler.verifyCodeExists(code)
                else:
                    raise ValueError("Code generation failed")
            return code
        except Exception as e:
            logging.info(e)
            raise e

    @staticmethod
    def verifyCodeGenerator(min_char, max_char):
        # allchar = string.ascii_letters + string.punctuation + string.digits
        allchar = string.ascii_letters + string.digits
        code = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        logging.info("This is your verification code : {0}".format(str(code)))
        return code

    @staticmethod
    def verifyCodeExists(code):
        try:
            Code_ = activation_data.objects.get(code=code)
        except(TypeError, ValueError, OverflowError, activation_data.DoesNotExist):
            Code_ = None
        if Code_ is not None:
            logging.info("Code: {0} is invalid.".format(str(code)))
            return True
        else:
            logging.info("Code: {0} is valid.".format(str(code)))
            return False

    @staticmethod
    def TelcoOperatorFinder(mobile_number):
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
    def sentSMSlogs(mobile_number, message, category):
        try:
            user = profile.objects.get(mobile_number=mobile_number)
        except(TypeError, ValueError, OverflowError, profile.DoesNotExist):
            user = None
        if user is None:
            logging.warning("Attempted to save sent SMS log to mobile number {0} which is not registered".format(str(mobile_number)))
            return False
        else:
            try:
                user = User.objects.get(pk=user.username_id)
                sms_log = sentSMSLogs(username_id=user.id, mobile_number=mobile_number, message_sent=message, category=category)
                sms_log.save()
                logging.info("Saved sent sms log for user {0}".format(str(mobile_number)))
                return True
            except Exception as e:
                logging.error("Failed to save sent sms log for user {0}".format(str(mobile_number)))
                logging.exception(e)
                return False
