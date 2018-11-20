from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from slugger import AutoSlugField

# Create your models here.
# CIRCLE_CHOICES = (
#     ('Daily', 'Daily.'),
#     ('Monthly', 'Monthly.'),
#     ('Q1', 'Q1.'),
#     ('Q2', 'Q2.'),
#     ('Q3', 'Q3.'),
#     ('Q4', 'Q4.'),
#     ('Yearly', 'Yearly.'),
#     ('Weekly', 'Weekly'),
# )
# contribution_intervals = models.CharField(max_length=3, choices=CIRCLE_CHOICES)


class Chama(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year_founded = models.CharField(max_length=255)
    maximum_members = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contribution_intervals = models.CharField(max_length=255)
    total_contributions = models.CharField(max_length=255)
    saved_amounts = models.CharField(max_length=255)
    twitter_link = models.CharField(max_length=255)
    facebook_link = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Chama'
        verbose_name_plural = 'Chamas'

    def __unicode__(self):
        return self.name


PLAN_CHOICES = (
    ('Free', 'Free'),
    ('Starter', 'Starter'),
    ('Bronze', 'Bronze'),
    ('Silver', 'Silver'),
    ('Platinum', 'Platinum'),
)


class plan_packages(models.Model):
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
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    def __unicode__(self):
        return self.name

