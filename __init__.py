# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2012 Duoshuo
#
__version__ = '0.1'

import os.path
import urllib
import urllib2
import warnings
import urlparse
import binascii
import hashlib
import hmac

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

HOST = 'dmyz.duoshuo.com/api'
#HOST = '127.0.0.1'

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
    def __init__(self, client_id=None, secret=None, version='1.0', **kwargs):
        self.client_id = client_id
        self.secret = secret
        if not secret:
            warnings.warn('You should pass ``secret``.')
        self.version = version
        #self._auth()
    
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
            return 'http://%s/%s?%s' % (HOST, 'oauth2', \
                urllib.urlencode(sorted(params.items())))
    
    def get_token(self, code=None, redirect_uri=None):
        if not redirect_uri:
            raise APIError('01', 'Invalid request: redirect_uri')
        elif not code:
            raise APIError('01', 'Invalid request: code')
        else:
            params = {'client_id': self.client_id, 'secret': self.secret, 'redirect_uri': redirect_uri, 'code': code}
            url = 'http://%s/%s?%s' % (HOST, 'token', \
                urllib.urlencode(sorted(params.items())))
            file = urllib.urlopen(url)
            
            #result = _parse_json(file.read())
            #conn.putrequest("POST", url)
            
    
    def get_duoshuo_comment_form(self):
        pass

    def setSecretKey(self, key):
        self.secret_key = key
    setKey = setSecretKey

    def setPublicKey(self, key):
        self.public_key = key
    
    def _auth(self):
        post_data = None if post_args is None else urllib.urlencode(post_args)
        file = urllib.urlopen("https://graph.facebook.com/" + path + "?" +
                              urllib.urlencode(args), post_data)
        try:
            response = _parse_json(file.read())
        finally:
            file.close()
        
def get_hash(url):
    urlparts = urlparse.urlparse(url)
    
    if urlparts.query:
        norm_url = '%s?%s' % (urlparts.path, urlparts.query)
    elif params:
        norm_url = '%s?%s' % (urlparts.path, get_normalized_params(params))
    else:
        norm_url = urlparts.path
        
    #params = urlparts.params
    print norm_url
    #return binascii.b2a_base64(hashlib.sha1(urlparts.params).digest())[:-1]