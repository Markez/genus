from __future__ import absolute_import, division, print_function, unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from slugger import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from django.db import models
from django.utils import six

# Create your models here.


class plan_packages(models.Model):
    FREE = 'free'
    STARTER = 'starter'
    BRONZE = 'bronze'
    SILVER = 'silver'
    PLATINUM = 'platinum'

    PLAN_CHOICES = (
        (FREE, _('free')),
        (STARTER, _('starter')),
        (BRONZE, _('bronze')),
        (SILVER, _('silver')),
        (PLATINUM, _('platinum')),
    )
    name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    chargable = models.BooleanField(default=True)
    charges = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    maximum_users = models.IntegerField(default=5)
    bulk_emails = models.IntegerField(default=0)
    bulk_sms = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='plan_package', unique=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('plan')
        verbose_name_plural = _('plans')

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        try:
            plan = self.name
        except ObjectDoesNotExist:
            plan = None
        return "{0}".format(plan)

    @property
    def persistent_id(self):
        return '{0}/{1}'.format(self.model_label(), self.id)

    @classmethod
    def model_label(cls):
        """
            Returns an identifier for this Django model class
            This is just the standard "<app_label>.<model_name" form.
        """
        return '{0}.{1}'.format(cls._meta.app_label, cls._meta.model_name)

    @classmethod
    def from_persistent_id(cls, persistent_id):
        """

        :param persistent_id:
        :return:
            Loads a plan from its persistent id::
            plan == plan_packages.from_persistent_id(plan_packages.persistent_id)

        """
        plan = None

        try:
            model_label, plan_packages_id = persistent_id.rsplit('/', 1)
            app_label, model_name = model_label.split('.')
            plan_cls = apps.get_model(app_label, model_name)
            if issubclass(plan_cls, plan_packages):
                plan = plan_cls.objects.filter(id=int(plan_packages_id)).first()
        except (ValueError, LookupError):
            pass

        return "{0}".format(plan)


class Chama(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    CIRCLE_CHOICES = (
        (DAILY, _('daily')),
        (WEEKLY, _('weekly')),
        (MONTHLY, _('monthly')),
        (YEARLY, _('yearly')),
    )
    FREE = 'free'
    STARTER = 'starter'
    BRONZE = 'bronze'
    SILVER = 'silver'
    PLATINUM = 'platinum'

    PLAN_CHOICES = (
        (FREE, _('free')),
        (STARTER, _('starter')),
        (BRONZE, _('bronze')),
        (SILVER, _('silver')),
        (PLATINUM, _('platinum')),
    )
    creator = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=13)
    name = models.CharField(max_length=255)
    year_founded = models.CharField(max_length=255)
    maximum_members = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contribution_intervals = models.CharField(
        max_length=255, choices=CIRCLE_CHOICES)
    total_contributions = models.CharField(max_length=255)
    saved_amounts = models.CharField(max_length=255)
    plan_package = models.CharField(
        max_length=255, choices=PLAN_CHOICES)
    twitter_link = models.CharField(max_length=255)
    facebook_link = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('chama')
        verbose_name_plural = _('chamas')

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        try:
            chamaa = self.name
        except ObjectDoesNotExist:
            chamaa = None
        return "{0}".format(chamaa)
