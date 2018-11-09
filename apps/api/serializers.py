from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterUserApiSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)


class RegistrationVeryPhoneApiSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)


class RequestPasswordResetCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)


class ValidatePasswordResetCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')
