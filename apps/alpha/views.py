import logging
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import ChamaForm
from .models import Chama, plan_packages
from django.contrib.auth.models import User
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
                form = ChamaForm(request.POST)
                current_user = request.user
                if form.is_valid():
                    # logging.info(form)
                    user = User.objects.get(username=current_user.username)
                    data = Chama()
                    data.creator_id = user.id
                    data.name = request.POST['name']
                    data.year_founded = request.POST['year_founded']
                    data.maximum_members = request.POST['maximum_members']
                    data.description = request.POST['description']
                    data.contribution_intervals = request.POST['contribution_intervals']
                    data.total_contributions = request.POST['total_contributions']
                    data.saved_amounts = request.POST['saved_amounts']
                    data.twitter_link = request.POST['twitter_link']
                    data.facebook_link = request.POST['facebook_link']
                    data.save()
                    logging.warning("Saved")
                    messages.add_message(request, messages.ERROR, "Chama has been created successfully")
                else:
                    logging.warning("Form posted is not valid")
                    pass
            else:
                form = ChamaForm()
                return render(request, 'alpha/body/newChama.html', {'form': form})
        else:
            logging.warning("User is not authenticated and is trying to create new chama")
            return redirect('%s?next=%s' % ('/a/user/login/', '/account/creating/newchama/'))
    except Exception as e:
        logging.exception(e)
        pass


def selectPlan(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                current_user = request.user
                logging.info("{}, wants to register a new chama under {} plan.".format(str(current_user.username), str(request.POST['plan'])))
                context = {
                    'form': ChamaForm(),
                    'plan': request.POST['plan']
                }
                return render(request, 'alpha/body/newChama.html', context)
            else:
                free = plan_packages.objects.get(slug="free")
                starter = plan_packages.objects.get(slug="starter")
                silver = plan_packages.objects.get(slug="silver")
                platinum = plan_packages.objects.get(slug="platinum")
                context = {
                    'free': free,
                    'starter': starter,
                    'silver': silver,
                    'platinum': platinum
                }
                return render(request, 'alpha/body/plan.html', context)
        else:
            logging.warning("User is not authenticated and is trying to create new chama")
            return redirect('%s?next=%s' % ('/a/user/login/', '/account/select/plan/'))
    except Exception as e:
        logging.exception(e)
        pass
