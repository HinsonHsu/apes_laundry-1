# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-09 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_categories_cities_price_rules_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories_cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.BigIntegerField()),
                ('category_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'categories_cities',
            },
        ),
    ]