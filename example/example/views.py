# encoding: utf8

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render
from accounts.models import UserProfile

import settings
import jwt
def home(request):
    duoshuo_jwt_token = None
    ctx = {
        'settings': settings,
    }
    if request.user.is_authenticated():
        ctx['profile'] = UserProfile.objects.get(user_id=request.user.id) #django 1.7没有get_profile

        # 实现JWT登录，参看：http://dev.duoshuo.com/docs/501e6ce1cff715f71800000d
        token = {       
            "short_name": settings.DUOSHUO_SHORT_NAME,
            "user_key": request.user.id, 
            "name": request.user.username
        }
        ctx['duoshuo_jwt_token'] = duoshuo_jwt_token = jwt.encode(token, settings.DUOSHUO_SECRET)

    response = TemplateResponse(request, 'home.html', ctx)
    response.set_cookie('duoshuo_token', duoshuo_jwt_token)
    return response
