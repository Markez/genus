from __future__ import absolute_import, division, print_function, unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import six

# Create your models here.

"""
  sent sms logs keeper models and it's various attributes
"""


# for user sent sms
class sentSMSLogs(models.Model):
    REG = "registration_code"
    RESET_PASSWORD_REQUEST = "password_reset_code"
    CATEGORY_CHOICES = (
        (REG, "registration_code"),
        (RESET_PASSWORD_REQUEST, "password_reset_code"),
    )
    username = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=13)
    message_sent = models.CharField(max_length=255)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Sent SMS'
        verbose_name_plural = 'Sent SMS'

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
        response = "{0}".format(phone)
        return response


class userActivities(models.Model):
    """
      Choices options for the activities and their states
    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    IN_PROGRESS = 'in_progress'
    SUSPENDED = 'suspended'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (ACTIVE, _('active')),
        (INACTIVE, _('inactive')),
        (IN_PROGRESS, _('in_progress')),
        (SUSPENDED, _('suspended')),
        (COMPLETED, _('completed')),
    )

    """
      Choices options for the activities and their states
    """

    RESET_PASSWORD = 'reset_password'
    USER_REGISTRATION = 'user_registration'
    CHANGE_PASSWORD = 'change_password'
    CREATE_CHAMA = 'create_chama'
    UPDATE_CHAMA = 'update_chama'
    CHOOSE_PLAN = 'choose_plan'
    CHANGE_PLAN = 'change_plan'

    ACTION_CHOICES = (
        (USER_REGISTRATION, _('user_registration')),
        (RESET_PASSWORD, _('reset_password')),
        (CHANGE_PASSWORD, _('change_password')),
        (CREATE_CHAMA, _('create_chama')),
        (UPDATE_CHAMA, _('update_chama')),
        (CHOOSE_PLAN, _('choose_plan')),
        (CHANGE_PLAN, _('change_plan')),
    )

    """
      user activities logger models and it's various attributes
    """

    username = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=13)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)
    token = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    state_changed_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-state_changed_on']
        verbose_name = _('activity')
        verbose_name_plural = _('activities')

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        try:
            deed = self.action
        except ObjectDoesNotExist:
            deed = None
        response = "{0}".format(deed)
        return response
