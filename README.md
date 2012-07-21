# Duoshuo Python SDK

本SDK支持用Python语言开发的网站，对其提供[多说]插件的支持。

# Requirements

Python 2.6+

Django 1.2+ (如果在Django中使用)

# Index

[Python Useage](#python-usage)

[Django useage](#django-usage)


# Python Usage

作为Python models来使用

## Core (`__init__`.py)

sdk核心功能： 交换token，生成授权链接，调用api接口

***

### 实例化duoshuoAPI

    from duoshuo import DuoshuoAPI

    code = reqeust.GET.get(code)

    api = DuoshuoAPI(short_name=YOUR_DUOSHUO_SHORTNAME, secret=YOUR_DUOSHUO_SECRET)

    `#例如要获取用户信息
    api.users.details(user_id=1)


更多API可以查看[多说开发文档](http://dev.duoshuo.com/docs "多说开发文档") 。

### 交换token

    code = reqeust.GET.get(code)

    token = ds.get_token(redirect_uri=redirect_uri, code=code)

### 生成oath链接

    auth_url = ds.get_url(redirect_uri=redirect_uri)


## Utils (utils.py)

多说常用处理： remote_auth字符串加密。

***
views.py:

    from duoshuo.utils import remote_auth
    sig = remote_auth(id=request.user.id, name=request.user.username, email=request.user.email)

template/xxx.html

    duoshuoQuery['remote_auth'] = {{ sig }}

## Widgets (widgets.py)

多说主要挂件：最新评论，最近访客

soon coming...

# Django Usage

作为Django app来使用

## 0. 安装duoshuo插件

	pip install duoshuo

	INSTALLED_APPS = (
		...
		'duoshuo',
	)


## 1. 导入已有数据

	python manager.py ds_import user

	python manager.py ds_import comment


## 2. 显示多说评论框

	{% load duoshuo %}