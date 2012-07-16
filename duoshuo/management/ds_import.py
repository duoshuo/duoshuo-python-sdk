# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import urllib
import urllib2

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Tell me wha\'s data you want synchronization (user/article/comment)')
        if args[0] == 'user':
            data = {
                'secret' : '7cea7aa4d7cab42a33d07abed43cbbc7',
                'short_name' : '56we',
            }

            api_url = 'http://api.duoshuo.com/users/import.json'
            users = User.objects.all()
            users_data = {}
            for user in users:
                avatar = user.get_profile().avatar and user.get_profile().avatar or ''
                if user.id == 1: user.username = u"比肩社区"

                data['users[%s][name]'% user.id] = user.username
                data['users[%s][email]'% user.id] = user.email
                data['users[%s][avatar]'% user.id] = 'http://tp2.sinaimg.cn/2300398305/180/5633531228/1'

            data = urllib.urlencode(data)
            response = urllib2.urlopen(api_url, data).read()
            print response

#        for poll_id in args:
#            try:
#                poll = Poll.objects.get(pk=int(poll_id))
#            except Poll.DoesNotExist:
#                raise CommandError('Poll "%s" does not exist' % poll_id)
#
#            poll.opened = False
#            poll.save()
