![Banner](https://raw.github.com/perchouli/img/master/banner-772x250.png)

# Duoshuo Python SDK

多说Python SDK支持用Python语言开发的网站，对其提供[多说]插件的支持。使用中遇到的问题请[到多说开发者中心提问](http://dev.duoshuo.com/threads/500c9c58a03193c12400000c "多说开发者中心") 。

# Requirements

Python 2.6+

Django 1.2+ (如果在Django中使用)

# Install

    python setup.py install

# Index

[Python Useage](#python-usage)

[Django useage](#django-usage)


# Python Usage

作为Python models来使用

### Core (__init__.py)

sdk核心功能： 交换token，生成授权链接，调用api接口

#### 实例化duoshuoAPI

    from duoshuo import DuoshuoAPI

    api = DuoshuoAPI(short_name=YOUR_DUOSHUO_SHORT_NAME, secret=YOUR_DUOSHUO_SECRET)

    #例如要获取用户信息
    api.users.details(user_id=1)


更多API可以查看[多说开发文档](http://dev.duoshuo.com/docs "多说开发文档") 。

#### 交换token
访问需要登录的接口时要先进行授权，采用OAuth2.0协议，Python SDK提供交换token的处理，实例化api后可以直接传入code来获取token：

    code = request.GET.get(code)

    token = api.get_token(redirect_uri=redirect_uri, code=code)


# Django Usage

作为Django app来使用

#### 0. 安装duoshuo插件

    # settings.py
    INSTALLED_APPS = (
        ...
        'duoshuo',
    )

    DUOSHUO_SECRET = '你的多说secret，在多说管理后台 - 设置 - 密钥'
    DUOSHUO_SHORT_NAME = '你的多说short name，比如你注册了example.duoshuo.com，short name就是example'

#### 1. 导入已有用户

    python manager.py ds_import user


#### 2. 显示多说评论框

    {% load duoshuo_tags %}

    {% duoshuo_comments %}

    #给多说评论框传递其他short name
    {% duoshuo_comments '其他short name' %}

