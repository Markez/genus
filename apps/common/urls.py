from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # django
    path('', views.public_home, name='open_home'),
]
