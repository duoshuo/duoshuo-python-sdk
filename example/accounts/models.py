# encoding: utf8
from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    duoshuo_id = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    avatar = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender=None, instance=None, created=False, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
        userprofile.save()
models.signals.post_save.connect(create_user_profile, sender=User)
