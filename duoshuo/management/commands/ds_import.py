# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import urllib
import urllib2

import settings

DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORTNAME", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Tell me wha\'s data you want synchronization (user/article/comment)')
        if not DUOSHUO_SHORT_NAME or not DUOSHUO_SECRET:
            raise CommandError('Before you can sync you need to set DUOSHUO_SHORT_NAME and DUOSHUO_SECRET')
        else:
            data = {
                'secret' : DUOSHUO_SECRET,
                'short_name' : DUOSHUO_SHORT_NAME,
            }
        if args[0] == 'user':
            #api_url = 'http://api.duoshuo.com/users/import.json'
            users = User.objects.all()
            users_data = {}
            for user in users:
                avatar = user.get_profile().avatar and user.get_profile().avatar or ''

                data['users[%s][name]'% user.id] = user.username
                data['users[%s][email]'% user.id] = user.email
                data['users[%s][avatar]'% user.id] = avatar

                print '[%s]%s' % (user.id, user.username) +' was success sync;'

            data = urllib.urlencode(data)
            #response = urllib2.urlopen(api_url, data).read()

        if args[0] == 'comment':
            comments = Comment.object.all()
