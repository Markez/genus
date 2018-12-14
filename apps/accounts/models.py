from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import six

# Create your models here.


# for user profile
class profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(unique=True, max_length=13)
    operator = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        try:
            phone = self.mobile_number
        except ObjectDoesNotExist:
            phone = None
        return "{0}".format(phone)


class activation_data(models.Model):
    username = models.CharField(max_length=255)
    mobile_number = models.CharField(default="notSet", max_length=13)
    code = models.CharField(unique=True, max_length=10)
    token = models.CharField(unique=True, max_length=255)
    status = models.CharField(default="unverified", max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Registration Token')
        verbose_name_plural = _('Registration Tokens')

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        try:
            res = "{0}, {1}".format(self.code, self.token)
        except ObjectDoesNotExist:
            res = None
        return "{0}".format(res)
