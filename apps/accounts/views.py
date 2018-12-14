import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from backend.accounts.processes import RegistrationHandler, PassResetHandler
from backend.common.processes import BaseHandler

from .forms import SetPasswordForm, SignupForm, forgotPasswordForm, passResetCodeVerify, smsCodeVerifyForm
from .tokens import account_activation_token

logging = logging.getLogger('accounts')


def reg_ister(request):
    try:
        form = SignupForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                mobile_number = request.POST.get('mnumber')
                response = BaseHandler.mobile_number_exists(mobile_number)
                if response is True:
                    messages.add_message(request, messages.ERROR, "Mobile number already exists")
                else:
                    logging.info('Ready to process registration')
                    user = form.save(commit=False)
                    RegistrationHandler.register_user(user, mobile_number)
                    context = {
                        'form': smsCodeVerifyForm(),
                        'person': mobile_number,
                    }

                    return render(request, 'alpha/accounts/activate_account.html', context)
        else:
            form = SignupForm()
        return render(request, 'alpha/accounts/signup.html', {'form': form})
    except Exception as e:
        logging.error(e)
        raise e


def activate_using_sms_code(request):
    try:
        if request.method == 'POST':
            form = smsCodeVerifyForm(request.POST)
            if form.is_valid():
                logging.info('Ready to process using code activation')
                mobile_number = request.POST.get('Mobile_Number')
                code = request.POST.get('Verification_Code')
                response = RegistrationHandler.sms_code_activation(mobile_number, code)
                if response == "error0":
                    messages.add_message(request, messages.ERROR,
                                         "The code provided is invalid")
                elif response == "error1":
                    messages.add_message(request, messages.ERROR,
                                         "Verification token invalid")
                elif response == "error2":
                    messages.add_message(request, messages.ERROR,
                                         "Phone number and Code provided are invalid")
                else:
                    login(request, response)
                    return redirect('account_dashboard')
        else:
            form = smsCodeVerifyForm()
        return render(request, 'alpha/accounts/activate_account.html', {'form': form})
    except Exception as e:
        logging.error(e)
        raise e


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def forgot_pass(request):
    try:
        if request.method == 'POST':
            form = forgotPasswordForm(request.POST)
            if form.is_valid():
                mobile_number = request.POST.get('Mobile_Number')
                response = BaseHandler.mobile_number_exists(mobile_number)
                if response is False:
                    messages.add_message(request, messages.ERROR, "Mobile number does not exists")
                else:
                    logging.info('Ready to process reset instructions')
                    response = PassResetHandler.process_reset_code(mobile_number)
                    if response is True:
                        context = {
                            'form': passResetCodeVerify(),
                            'person': mobile_number,
                        }

                        return render(request, 'alpha/accounts/activate_password_reset.html', context)
                    else:
                        messages.add_message(request, messages.ERROR,
                                             "Request failed, please try again!")
        else:
            form = forgotPasswordForm()
        return render(request, 'alpha/accounts/forgot_password.html', {'form': form})
    except Exception as e:
        logging.error(e)
        raise e


def forgot_pass_verification(request):
    try:
        if request.method == 'POST':
            form = passResetCodeVerify(request.POST)
            if form.is_valid():
                mobile_number = request.POST.get('Mobile_Number')
                code = request.POST.get('Verification_Code')
                response = BaseHandler.mobile_number_exists(mobile_number)
                if response is False:
                    messages.add_message(request, messages.ERROR, "Mobile number does not exists")
                else:
                    response = RegistrationHandler.sms_code_activation(mobile_number, code)
                    if response == "error0":
                        messages.add_message(request, messages.ERROR,
                                             "The code provided is invalid")
                    elif response == "error1":
                        messages.add_message(request, messages.ERROR,
                                             "Verification token invalid")
                    elif response == "error2":
                        messages.add_message(request, messages.ERROR,
                                             "Phone number and Code provided are invalid")
                    else:
                        logging.info("Ready to process password reset")
                        context = {
                            'form': SetPasswordForm(),
                            'person': mobile_number,
                        }

                        return render(request, 'alpha/accounts/password_reset.html', context)
        else:
            form = passResetCodeVerify()
        return render(request, 'alpha/accounts/activate_password_reset.html', {'form': form})
    except Exception as e:
        logging.error(e)
        raise e


def pass_reset(request):
    try:
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                mobile_number = request.POST.get('Mobile_Number')
                new_password = request.POST.get('New_Password')
                confirm_password = request.POST.get('Confirm_New_Password')
                response = BaseHandler.mobile_number_exists(mobile_number)
                if response is False:
                    messages.add_message(request, messages.ERROR, "Mobile number does not exists")
                else:
                    logging.info('Ready to reset password')
                    min_length = 8
                    if new_password != confirm_password:
                        messages.add_message(request, messages.ERROR, "Two passwords do not match")
                    elif len(new_password) < min_length:
                        messages.add_message(request, messages.ERROR,
                                             "This password must contain at least 8 characters.")
                    else:
                        response = PassResetHandler.set_new_password(mobile_number, new_password)
                        if response is True:
                            return redirect('core_login')
                        else:
                            messages.add_message(request, messages.ERROR, str(response))
                context = {
                    'form': SetPasswordForm(),
                    'person': mobile_number,
                }
                return render(request, 'alpha/accounts/password_reset.html', context)
        else:
            logging.info("This kind of request is not acceptable")
            return HttpResponse("This is not acceptable")
    except Exception as e:
        logging.error(e)
        raise e
