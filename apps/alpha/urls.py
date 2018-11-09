from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

urlpatterns = [
    # django
    path('dashboard', views.dash_board, name='account_dashboard'),
    path('getting/started/', views.starter, name='account_start'),
    path('creating/newchama/', views.newChama, name='account_create_chama'),
    #
]
