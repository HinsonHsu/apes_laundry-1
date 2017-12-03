# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.
class Prices(models.Model):
    price1 = models.FloatField()
    price2 = models.FloatField()
    price3 = models.FloatField()
    price4 = models.FloatField()
    price5 = models.FloatField()
    price6 = models.FloatField()
    product_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        app_label = 'products'
        db_table = 'prices'
class Price_rules(models.Model):
    grade = models.IntegerField()
    city_id = models.BigIntegerField()
    category_id = models.BigIntegerField()
    from_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'products'
        db_table = 'price_rules'

class Products(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    is_del = models.BooleanField()
    category_id = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'products'
        db_table = 'products'
class Categories(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    is_del = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'products'
        db_table = 'categories'
class Categories_cities(models.Model):
    city_id = models.BigIntegerField()
    category_id = models.BigIntegerField()
    class Meta:
        app_label = 'prodcuts'
        db_table = 'categories_cities'
class Cities(models.Model):
    name = models.CharField(max_length=255)
    is_del = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'products'
        db_table = 'cities'