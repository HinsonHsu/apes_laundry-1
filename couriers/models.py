# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# from users.models import User

# Create your models here.
class Courier(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    idcard_url = models.CharField(max_length=20)
    health_url = models.CharField(max_length=20)
    workplace = models.CharField(max_length=50)
    city_id = models.IntegerField(default=None)
    is_locked = models.BooleanField()
    is_checked = models.BooleanField()
    create_at = models.DateField()
    update_at = models.DateField()
    user_back_id = models.IntegerField()

    class Meta:
        app_label = 'couriers'
        # db_table = 'couriers'