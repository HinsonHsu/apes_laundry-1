# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Order(models.Model):
    ordersn = models.IntegerField()
    user_id = models.IntegerField()
    address = models.CharField(max_length=255, default="1")

    exp_date = models.DateTimeField()
    total_price = models.IntegerField()
    status = models.IntegerField(null=True)
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
    class Meta:
        app_label = 'orders'
        db_table = 'order_items'
