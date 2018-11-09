"""safaribet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('user/register/', views.RegisterUsersApi.as_view(), name='register_user'),
    path('user/register/verify/phone/', views.RegistrationVeryPhone.as_view(), name='registration_verifyPhone_user'),
    path('user/password/resetCode/', views.requestPasswordResetCode.as_view(), name='password_reset_code'),
    path('user/password/resetCode/validate/', views.validatePasswordResetCode.as_view(),
         name='password_validate_reset_code'),
    path('user/password/reset/', views.passwordReset.as_view(), name='password_reset'),
    path('user/viewSet/list/', views.UserViewSet.as_view({'get': 'list'}), name='user'),
    path('user/viewSet/detail/', views.UserViewSet.as_view({'get': 'retrieve'}), name='user'),
]
