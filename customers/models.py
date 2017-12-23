# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.
class CustomerAddress(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    sex = models.BooleanField(default=True)  # 1 男 0 女
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


class Customer_card(models.Model):
    real_money = models.FloatField()
    fake_money = models.FloatField()
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'customers'
        db_table = 'user_cards'


class Customer_card_log(models.Model):
    kind = models.IntegerField()
    real_money = models.FloatField()
    fake_money = models.FloatField()
    loggable_type = models.CharField(max_length=20, null=True)
    loggable_id = models.IntegerField()
    user_card_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'customers'
        db_table = 'user_card_logs'

class Customer_card_charge_settings(models.Model):
    min = models.FloatField()
    money_give = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'customers'
        db_table = 'user_card_charge_settings'
class Coupon(models.Model):
    customer_id = models.IntegerField()
    discount = models.FloatField()
    premise = models.FloatField()
    is_active = models.IntegerField()
    used_at = models.DateTimeField(default=timezone.now)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = 'customers'
        db_table = 'coupons'