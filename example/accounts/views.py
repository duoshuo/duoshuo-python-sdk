# encoding: utf8

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import  HttpResponseRedirect
from django.shortcuts import render

from duoshuo import DuoshuoAPI

from example.settings import DUOSHUO_SHORT_NAME, DUOSHUO_SECRET
from .models import UserProfile

import random

def callback(request):
    code = request.GET.get('code')
    api = DuoshuoAPI(short_name=DUOSHUO_SHORT_NAME, secret=DUOSHUO_SECRET)

    response = api.get_token(code=code)

    if response.has_key('user_key'): #此多说账号在本站已经注册过了，直接登录
        user = User.objects.get(pk=int(response['user_key']))
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    else: #此多说账号在本站未注册，添加一个用户
        response = api.users.profile(user_id=response['user_id'])['response']
        username = response['name']
        if User.objects.filter(username=username).count():
            username = username + str(random.randrange(1,9)) #如果多说账号用户名和本站用户名重复，就加上随机数字

        tmp_password = ''.join([random.choice('abcdefg&#%^*f') for i in range(8)]) #随机长度8字符做密码
        new_user = User.objects.create_user(username=username, email='user@example.com', password=tmp_password) #默认密码和邮箱，之后让用户修改
        
        userprofile = UserProfile.objects.get(user=new_user)
        userprofile.duoshuo_id = response['user_id'] #把返回的多说ID存到profile
        userprofile.avatar = response['avatar_url']
        userprofile.save()

        user = authenticate(username=username, password=tmp_password)
        login(request, user)
    context = {}
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.user.is_authenticated():
            user = request.user
        else:
            user = User.objects.create_user(username=username, email=email, password=password)

        api = DuoshuoAPI(short_name=DUOSHUO_SHORT_NAME, secret=DUOSHUO_SECRET)

        # 把本站用户导入多说，参看：http://dev.duoshuo.com/docs/51435552047fe92f490225de
        response = api.users.imports(data={
            'users[0][user_key]' : user.id,
            'users[0][name]': username,
            'users[0][email]': email,
        })['response']

        user_profile = UserProfile.objects.get(user=user)
        user_profile.duoshuo_id = int(response[str(user.id)])
        user_profile.save()

        if not request.user.is_authenticated():
            login_user = authenticate(username=username, password=password)
            login(request, login_user)

        return HttpResponseRedirect('/')
