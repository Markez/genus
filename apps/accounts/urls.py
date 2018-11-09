from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

urlpatterns = [
    # django
    path('user/login/', auth_views.LoginView.as_view(template_name='alpha/accounts/login.html'), name='core_login'),
    path(
        'user/change-password/',
        auth_views.PasswordChangeView.as_view(template_name='alpha/accounts/change-password.html'),
        name='password_reset'),
    path('user/logout/', auth_views.LogoutView.as_view(), {'next_page': 'core_login'}, name='core_logout'),
    path('user/register/', views.reg_ister, name='core_register'),
    path('user/forgot-password/', views.forgot_pass, name='core_forgot_password'),
    path('user/forgot-password/reset/verification/', views.forgot_pass_verification, name='core_pass_reset_activation'),
    path('user/forgot-password/reset/request/', views.pass_reset, name='core_pass_reset'),
    path('user/activate/', views.activate_using_sms_code, name='core_sms_activation'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
]
