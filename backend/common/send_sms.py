import logging
import africastalking
from decouple import config

logging = logging.getLogger("sms_sender")


class SendSMSHandler:
    @staticmethod
    def africaStalkingSMS(mobile_number, message):
        username = config('africa_username')
        api_key = config('africa_api_key')
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        phone = "+254"+mobile_number
        try:
            response = sms.send(message, [phone])
            return(response)
        except Exception as e:
            logging.exception('Encountered an error while sending: {0}'.format(str(e)))
            pass
