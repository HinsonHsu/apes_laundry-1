# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# from users.models import User

# Create your models here.
class Courier(models.Model):
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    idcard_url = models.CharField(max_length=20, null=True)
    health_url = models.CharField(max_length=20, null=True)
    workplace = models.CharField(max_length=50, null=True)
    city_id = models.IntegerField(null=True)
    is_locked = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    user_back_id = models.IntegerField(null=True)

    class Meta:
        app_label = 'couriers'
        db_table = 'couriers'

