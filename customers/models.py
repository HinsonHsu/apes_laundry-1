# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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