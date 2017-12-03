# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-03 01:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('idcard_url', models.CharField(max_length=20, null=True)),
                ('health_url', models.CharField(max_length=20, null=True)),
                ('workplace', models.CharField(max_length=50, null=True)),
                ('city_id', models.IntegerField(null=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('is_checked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_back_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'couriers',
            },
        ),
    ]
