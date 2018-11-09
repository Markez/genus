from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


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
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __unicode__(self):
        return self.mobile_number


class activation_data(models.Model):
    # username = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(default="notSet", max_length=13)
    code = models.CharField(unique=True, max_length=10)
    token = models.CharField(unique=True, max_length=255)
    status = models.CharField(default="unverified", max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Registration Token'
        verbose_name_plural = 'Registration Tokens'

    def __unicode__(self):
        return "{0}, {1}".format(self.code, self.token)
