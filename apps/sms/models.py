from __future__ import absolute_import, division, print_function, unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import models
from django.utils import six


# Create your models here.
"""
AfricaStalking sms usage
"""

"""
    Saving Africa's Talking sent sms responses to keep record of the costs for internal use
"""


class africasTalkingResponses(models.Model):
    username = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=13)
    sms_target = models.CharField(max_length=255)
    response_message = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    statusCode = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    messageId = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'AfricaStalking SMS Response'
        verbose_name_plural = 'AfricaStalking SMS Responses'

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


class AfrikaStalkingSMSMetrics(models.Model):
    sms_target = models.CharField(max_length=100)
    total_sent = models.IntegerField(default=0)
    total_cost = models.FloatField(default=0.00000)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'AfricaStalking SMS Cost Metric'
        verbose_name_plural = 'AfricaStalking SMS Cost Metrics'

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        try:
            target = self.sms_target
        except ObjectDoesNotExist:
            target = None
        response = "{0}".format(target)
        return response
