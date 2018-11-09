from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# for user sent sms
class sentSMSLogs(models.Model):
    REG = "Registration code"
    RESET_PASSWORD_REQUEST = "Password reset code"
    CATEGORY_CHOICES = (
        (REG, "Registration code"),
        (RESET_PASSWORD_REQUEST, "Password reset code"),
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=13)
    message_sent = models.CharField(max_length=255)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Sent SMS'
        verbose_name_plural = 'Sent SMS'

    def __unicode__(self):
        return "{0}".format(self.mobile_number)
