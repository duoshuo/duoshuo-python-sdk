# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

AUTH_PROFILE_MODULE = getattr(settings, "AUTH_PROFILE_MODULE")

class Site(models.Model):
    use_images = models.BooleanField(default=True)
    short_name = models.CharField(max_length=40)

class User(models.Model):
    user = models.ForeignKey(User)
    identifier = models.CharField(max_length=32)

def register(identifier):
    #app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    model = models.get_model(app_label, model_name)
    qs = model._default_manager.all()
    print model