from rest_framework.views import APIView
from . import serializers
import logging
from rest_framework.decorators import action
from django.http import JsonResponse
from backend.accounts.processes import RegistrationHandler, PassResetHandler
from backend.common.processes import BaseHandler
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

logging = logging.getLogger('apis_view')


class RegisterUsersApi(APIView):
    """
    New user registration
    """
    def get_serializer(*args, **kwargs):
        return serializers.RegisterUserApiSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {}
        try:
            serializer = RegisterUsersApi().get_serializer(
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            mobile_number = serializer.validated_data['mobile_number']
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']
            logging.info(mobile_number)
            logging.info(username)
            logging.info(password)
            res_ = BaseHandler.mobile_number_exists(mobile_number)
            if res_ is True:
                status = 400
                response['status'] = False
                response['code'] = 1
                response['message'] = "Mobile number already exists"
            else:
                user = User()
                user.username = username
                user.set_password(password)
                RegistrationHandler.register_user_api(user, mobile_number, username)
                status = 201
                response['status'] = True
                response['code'] = 0
                response['message'] = "Registration was successful"
        except Exception as e:
            logging.exception(e)
            response['status'] = False
            response['code'] = 1
            response['message'] = str(e)
            status = 400

        return JsonResponse(response, status=status)


class RegistrationVeryPhone(APIView):
    """
    Verifying code sent to the set phone number
    """
    def get_serializer(*args, **kwargs):
        return serializers.RegistrationVeryPhoneApiSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {}
        try:
            serializer = RegistrationVeryPhone().get_serializer(
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            mobile_number = serializer.validated_data['mobile_number']
            code = serializer.validated_data['code']
            logging.info(mobile_number)
            logging.info(code)
            res_ = BaseHandler.mobile_number_exists(mobile_number)
            if res_ is True:
                response_ = RegistrationHandler.sms_code_activation(mobile_number, code)
                # return JsonResponse(
                #     RegistrationHandler.smsCodeAPIActivation(
                #         serializer.validated_data['mobile_number'],
                #         serializer.validated_data['code']
                #     ), safe=False
                # )
                if response_ == "error0":
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "The code provided is invalid"
                elif response_ == "error1":
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "Verification token invalid"
                elif response_ == "error2":
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "Phone number and Code provided are invalid"
                else:
                    status = 201
                    response['status'] = True
                    response['code'] = 0
                    response['message'] = "Account phone verified successfully"
            else:
                status = 400
                response['status'] = False
                response['code'] = 1
                response['message'] = "Mobile number not registered"
        except Exception as e:
            logging.exception(e)
            response['status'] = False
            response['code'] = 1
            response['message'] = str(e)
            status = 400

        return JsonResponse(response, status=status)


class requestPasswordResetCode(APIView):
    """
    Requesting for password reset code
    """
    def get_serializer(*args, **kwargs):
        return serializers.RequestPasswordResetCodeSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {}
        try:
            serializer = requestPasswordResetCode().get_serializer(
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            mobile_number = serializer.validated_data['mobile_number']
            logging.info(str(mobile_number))
            res_ = BaseHandler.mobile_number_exists(mobile_number)
            if res_ is True:
                response_ = PassResetHandler.process_reset_code(mobile_number)
                if response_ is True:
                    status = 201
                    response['status'] = True
                    response['code'] = 0
                    response['message'] = [
                        {
                            "body": "Password reset code sent via sms",
                            "user": mobile_number
                        }
                    ]
                else:
                    status = 500
                    response['status'] = True
                    response['code'] = 1
                    response['message'] = "Password reset code request failed. PLease try again !!"
            else:
                status = 400
                response['status'] = False
                response['code'] = 1
                response['message'] = "Mobile number not registered"
        except Exception as e:
            logging.exception(e)
            response['status'] = False
            response['code'] = 1
            response['message'] = str(e)
            status = 400

        return JsonResponse(response, status=status)


class validatePasswordResetCode(APIView):
    """
    Validating reset code sent via sms
    """
    def get_serializer(*args, **kwargs):
        return serializers.ValidatePasswordResetCodeSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {}
        try:
            serializer = validatePasswordResetCode().get_serializer(
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            mobile_number = serializer.validated_data['mobile_number']
            code = serializer.validated_data['code']
            logging.info(str(mobile_number))
            res_ = BaseHandler.mobile_number_exists(mobile_number)
            if res_ is True:
                response_ = RegistrationHandler.sms_code_activation(mobile_number, code)
                if response_ == "error0":
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "The code provided is invalid"
                elif response_ == "error1":
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "Verification token invalid"
                elif response_ == "error2":
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "Phone number and Code provided are invalid"
                else:
                    status = 201
                    response['status'] = True
                    response['code'] = 0
                    response['message'] = [
                        {
                            "body": "Account phone verified successfully",
                            "user": mobile_number
                        }
                    ]
            else:
                status = 400
                response['status'] = False
                response['code'] = 1
                response['message'] = "Mobile number not registered"
        except Exception as e:
            logging.exception(e)
            response['status'] = False
            response['code'] = 1
            response['message'] = str(e)
            status = 400

        return JsonResponse(response, status=status)


class passwordReset(APIView):
    """
    Resetting new password
    """
    def get_serializer(*args, **kwargs):
        return serializers.PasswordResetSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {}

        try:
            serializer = passwordReset().get_serializer(
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            mobile_number = serializer.validated_data['mobile_number']
            new_password = serializer.validated_data['new_password']
            confirmed_password = serializer.validated_data['confirm_password']
            logging.info(str(mobile_number))
            res_ = BaseHandler.mobile_number_exists(mobile_number)
            if res_ is True:
                logging.info('Ready to reset password')
                min_length = 8
                if new_password != confirmed_password:
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "Two passwords do not match"
                elif len(new_password) < min_length:
                    status = 400
                    response['status'] = False
                    response['code'] = 1
                    response['message'] = "This password must contain at least 8 characters."
                else:
                    reply = PassResetHandler.set_new_password(mobile_number, new_password)
                    if reply is True:
                        status = 201
                        response['status'] = True
                        response['code'] = 0
                        response['message'] = [
                            {
                                "body": "Password reset was successful",
                                "user": mobile_number
                            }
                        ]
                    else:
                        status = 500
                        response['status'] = False
                        response['code'] = 1
                        response['message'] = "Something went wrong. Please try again !!"
            else:
                status = 400
                response['status'] = False
                response['code'] = 1
                response['message'] = "Mobile number not registered"
        except Exception as e:
            logging.exception(e)
            response['status'] = False
            response['code'] = 1
            response['message'] = str(e)
            status = 400

        return JsonResponse(response, status=status)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(detail=True, methods=['post'])
    def list(self, request):
        queryset = User.objects.all().order_by('-last_login')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
