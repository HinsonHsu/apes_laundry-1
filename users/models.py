# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if extra_fields.has_key('email') and extra_fields['email']:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)
#用户
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, null=True)
    password = models.CharField(max_length=128, null=True)
    email = models.EmailField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        return self.username