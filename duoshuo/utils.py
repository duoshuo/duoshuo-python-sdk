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

from duoshuo import DuoshuoAPI

API = 'http://api.duoshuo.com/oauth2/authorize'
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)
DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORTNAME", None)

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


def sync_article(article):
    userprofile = request.user.get_profile()
    if userprofile.duoshuo_id:
        author_id = userprofile.duoshuo_id
    else:
        author_id = 0

    api_url = 'http://api.duoshuo.com/threads/sync.json'
    #TODO: get article url from urls.py
    url_hash = hashlib.md5(article.url).hexdigest()
    data = urllib.urlencode({
        'short_name' : DUOSHUO_SHORT_NAME,
        'source_thread_id' : article.id,
        'url' : article.url,
        'url_hash' : url_hash,
        'author_id' : author_id
    })
    
    response = json.loads(urllib2.urlopen(api_url, data).read())['response']
    return response

def sync_user(user):
    data['users[%s][name]'% user.id] = user.username
    data['users[%s][email]'% user.id] = user.email

    api = DuoshuoAPI()
    response = api.users.import(user)

    return response

def get_url(self, redirect_uri=None):
    if not redirect_uri:
        raise ValueError('Missing required argument: redirect_uri')
    else:
        params = {'client_id': self.short_name, 'redirect_uri': redirect_uri, 'response_type': 'code'}
        return '%s://%s/oauth2/%s?%s' % (URI_SCHEMA, HOST, 'authorize', \
            urllib.urlencode(sorted(params.items())))

def sync_comment():
    pass
