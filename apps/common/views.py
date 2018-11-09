from django.shortcuts import render
from django.contrib.auth import logout
import logging
# Create your views here.
logging = logging.getLogger('common')


def public_home(request):
    try:
        if request.method == 'GET':
            return render(request, 'alpha/common/home.html')
        elif request.method == 'POST':
            logging.info('Ready to process from common home')
            pass
        else:
            logging.error("Requested method not recognized from common home")
    except Exception as e:
        logging.error(e)
        raise e
