# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
多说API测试文件。作为通用的Python程序，没有使用Django的TestCase
"""
import os
import unittest
os.sys.path.append('/home/perchouli/duoshuo-python-sdk/')

import duoshuo

class DuoshuoAPITest(unittest.TestCase):
    DUOSHUO_SHORT_NAME = 'test'
    DUOSHUO_SECRET_KEY = 'a'*64

    HOST = duoshuo.HOST
    
    def test_host(self):
        host = self.HOST
        self.assertEqual(host + 'api.duoshuo.com')


    def test_resource(self):
        pass
        #rs = duoshuo.Resource(INTERFACES)

if __name__ == '__main__':
    unittest.main()