import logging

from django.contrib.auth import logout
from django.shortcuts import redirect, render

# Create your views here.
logging = logging.getLogger('alpha')


def dash_board(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'GET':
                return render(request, 'alpha/body/dashboard.html')
            elif request.method == 'POST':
                logging.info('Ready to process registration')
                pass
            else:
                logging.warning("Registration request method not recognized")
        else:
            logging.warning("User is not authenticated and is trying to access dashboard")
            return redirect('%s?next=%s' % ('/a/user/login/', '/account/dashboard/'))
    except Exception as e:
        logging.exception(e)
        pass


def starter(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                logging.info('Ready to process any starter post')
                pass
            else:
                return render(request, 'alpha/body/index.html')
        else:
            logging.warning("User is not authenticated and is trying to access dashboard")
            return redirect('%s?next=%s' % ('/a/user/login/', '/account/getting/started/'))

    except Exception as e:
        logging.exception(e)
        pass


def newChama(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                pass
            else:
                return render(request, 'alpha/body/newChama.html')
        else:
            logging.warning("User is not authenticated and is trying to create new chama")
            return redirect('%s?next=%s' % ('/a/user/login/', '/account/creating/newchama/'))
    except Exception as e:
        logging.exception(e)
        pass
