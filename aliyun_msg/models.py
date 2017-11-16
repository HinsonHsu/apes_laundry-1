# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.
class PhoneCaptcha(models.Model):
    phone = models.CharField(max_length=20, unique=False, null=False)
    code = models.CharField(max_length=10, unique=False, null=False)
    type = models.IntegerField()
    is_sent = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)
