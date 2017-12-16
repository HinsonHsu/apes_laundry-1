# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from customers.models import Customer
# Create your models here.
class Order(models.Model):
    ordersn = models.IntegerField()
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=255, null=True)
    courier_id = models.IntegerField(null=True)
    courier_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255, default="1")
    exp_date = models.DateTimeField()
    total_price = models.IntegerField()
    target_station_id = models.IntegerField(null=True)
    # 1 已下单 2 已接单 3 已确认 4 已支付 5 已取消
    status = models.IntegerField(null=True)
    city_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    courier_status = models.IntegerField(null=True)
    voucher_status = models.IntegerField(null=True)
    cleaning_status = models.IntegerField(null=True)
    class Meta:
        app_label = 'orders'
        db_table = 'orders'

class Order_item(models.Model):
    ordersn = models.IntegerField()
    product_id = models.IntegerField()
    price = models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = 'orders'
        db_table = 'order_items'
