# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2012 Duoshuo
#
__version__ = '0.1'

import urllib
import urllib2
import warnings
import urlparse
import hashlib
import settings

try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)

try:
    import Cookie
except ImportError:
    import https.cookies as Cookie #python 3.0

HOST = 'api.duoshuo.com/oauth2'
DUOSHUO_CLIENT_ID = getattr(settings, "DUOSHUO_CLIENT_ID", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

class APIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '%s: %s' % (self.code, self.message)

class Result(object):
    def __init__(self, response, cursor=None):
        self.response = response
        self.cursor = cursor or {}

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, repr(self.response))

    def __iter__(self):
        for r in self.response:
            yield r

    def __len__(self):
        return len(self.response)

    def __getslice__(self, i, j):
        return list.__getslice__(self.response, i, j)

    def __getitem__(self, key):
        return list.__getitem__(self.response, key)

    def __contains__(self, key):
        return list.__contains__(self.response, key)


class DuoshuoAPI(object):
    def __init__(self, client_id=DUOSHUO_CLIENT_ID, secret=DUOSHUO_SECRET, version='1.0', **kwargs):
        self.client_id = client_id
        self.secret = secret
        if not secret:
            warnings.warn('You should pass ``secret``.')
        self.version = version
    
    def __call__(self, **kwargs):
        print self.secret_key

    def _request(self, **kwargs):
        raise SyntaxError('You cannot call the API without a resource.')

    def _get_key(self):
        return self.secret
    key = property(_get_key)

    def api(self, action, params=None):
        cookies = Cookie.SerialCookie()
        if cookies:
            print action
        else:
            raise APIError('02', 'Unauthorized client: please get_token')
            
    def get_url(self, redirect_uri=None):
        if not redirect_uri:
            raise APIError('01', 'Invalid request: redirect_uri')
        else:
            params = {'client_id': self.client_id, 'redirect_uri': redirect_uri, 'response_type': 'code'}
            return 'http://%s/%s?%s' % (HOST, 'authorize', \
                urllib.urlencode(sorted(params.items())))
    
    def get_token(self, code=None):
        if not code:
            raise APIError('01', 'Invalid request: code')
        #elif not redirect_uri:
        #    raise APIError('01', 'Invalid request: redirect_uri')
        else:
            #params = {'client_id': self.client_id, 'secret': self.secret, 'redirect_uri': redirect_uri, 'code': code}
            params = {'code': code}
            data = urllib.urlencode(params)
            url = 'http://%s/%s' % (HOST, 'access_token')#, \
                #urllib.urlencode(sorted(params.items())))
            request = urllib2.Request(url)
            response = urllib2.build_opener(urllib2.HTTPCookieProcessor()).open(request, data)
            #file = urllib.urlopen(url)
            #print 'url: '+url + '\r\ndata: ' + data
            return eval(response.read())
    
    def get_duoshuo_comment_form(self):
        pass

    def setSecretKey(self, key):
        self.secret_key = key
    setKey = setSecretKey

    def setPublicKey(self, key):
        self.public_key = key
