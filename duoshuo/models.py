# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class DuoshuoUser(models.Model):
	user = models.ForeignKey(User)
	duoshuo_id = models.IntegerField(default=0)
	