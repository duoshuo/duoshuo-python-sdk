# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

AUTH_PROFILE_MODULE = getattr(settings, "AUTH_PROFILE_MODULE")

class Site(models.Model):
    use_images = models.BooleanField(default=True)
    short_name = models.CharField(max_length=40)

class Auth(models.Model):
    user = models.ForeignKey(User)
    identifier = models.CharField(max_length=32)

    