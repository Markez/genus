"""genus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.contrib import admin
from decouple import config
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from django.views.generic.base import RedirectView

public_apis = [
    path('v1/api/', include('apps.api.urls')),
]

schema_view = get_swagger_view(title='GENUS APIs', patterns=public_apis)
# schema_view = get_swagger_view(title='GENUS APIs')
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

internal_apis = [
    path('favicon.ico', favicon_view),
    path('', include('apps.common.urls')),
    path('a/', include('apps.accounts.urls')),
    path('account/', include('apps.alpha.urls')),
    path('g-apis/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/portal/', admin.site.urls),
    path('v1/jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('v1/jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('silk', include('silk.urls', namespace='silk')),
    path('v1/docs/', schema_view, name='api_load_view'),
]

urlpatterns = internal_apis + public_apis
admin.site.site_header = config('admin_site_site_header')
admin.site.site_title = config('admin_site_site_title')
admin.site.index_title = config('admin_site_index_title')
# admin.site.unregister(User)
# admin.site.unregister(Group)
admin.site.disable_action('delete_selected')
