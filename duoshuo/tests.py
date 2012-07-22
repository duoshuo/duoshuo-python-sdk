# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
多说API测试文件。作为通用的Python程序，没有使用Django的TestCase
"""
import os
import unittest
os.sys.path.append('/home/perchouli/duoshuo-python-sdk/')

import duoshuo

import utils

class DuoshuoAPITest(unittest.TestCase):
    DUOSHUO_SHORT_NAME = 'example'
    DUOSHUO_SECRET = 'a'*64
    API = duoshuo.DuoshuoAPI(short_name=DUOSHUO_SHORT_NAME, secret=DUOSHUO_SECRET)

    def test_host(self):
        api = self.API
        host = api.host
        self.assertEqual(host, 'api.duoshuo.com')


    def test_get_url(self):
        redirect_uri = 'example.com'
        api = self.API
        url = utils.get_url(api, redirect_uri=redirect_uri)
        print url
        self.assertEqual(url,
            'http://%s/oauth2/authorize?client_id=%s&redirect_uri=%s&response_type=code' % 
            ( api.host, self.DUOSHUO_SHORT_NAME, redirect_uri)
        )

    def test_token(self):
        api = self.API
        response = api.get_token(code='c'*32)
        
        #print response

    def test_user_api(self):
        api = self.API
        response = api.users.details(user_id=1)
        user_id = response['user_id']
        self.assertEqual(int(user_id), 1)

if __name__ == '__main__':
    unittest.main()