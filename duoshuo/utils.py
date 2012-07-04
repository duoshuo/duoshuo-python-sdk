# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2012 Duoshuo

import binascii
import base64
import hashlib
import hmac
import time
import urllib
import urllib2
import urlparse
import json

API = 'http://api.duoshuo.com/oauth2/authorize'
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

"""
实现Remote Auth后可以在评论框显示本地身份
Use:
    views.py: sig = remote_auth(id=request.user.id, name=request.user.username, email=request.user.email)
    template/xxx.html: duoshuoQuery['remote_auth'] = {{ sig }}
"""
def remote_auth(user_id, name, email, url=None, avatar=None):
    data = json.dumps({
        'id': user_id,
        'name': name,
        'email': email,
        'url': url,
        'avatar': avatar,
    })
    message = base64.b64encode(data)
    timestamp = int(time.time())
    sig = hmac.HMAC(DUOSHUO_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
    return sig


def sync_article(thread):
    pass

def sync_user():
    users = User.objects.all()
    url = API
    user_list = []
    for user in users:
        user_list.append(user.username)
    
    #request = urllib2.Request(url, '', {'User-Agent': 'duoshuo-python-sdk'})
    data = urllib.urlencode({
                'client_id': '3076981980',
                'response_type': 'code',
            
            })
    request = urllib2.urlopen( '%s?%s' % (API, data))
    print request.read()

def sync_comment():
    pass
