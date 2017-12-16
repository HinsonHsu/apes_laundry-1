# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.
class CustomerAddress(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    sex = models.BooleanField(default=True)#1 男 0 女
    address = models.CharField(max_length=50)
    door_number = models.CharField(max_length=20)
    user_id = models.IntegerField()
    class Meta:
        app_label = 'customers'
        db_table = 'customeraddress'
class Customer(models.Model):
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    user_back_id = models.IntegerField(null=True)

    class Meta:
        app_label = 'customers'
        db_table = 'customers'