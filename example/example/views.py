# encoding: utf8

from django.template.response import TemplateResponse

from accounts.models import UserProfile

import settings

def home(request):
    ctx = {
        'settings': settings,
    }
    if request.user.id != None:
        ctx['profile'] = UserProfile.objects.get(user_id=request.user.id) #django 1.7没有get_profile
    return TemplateResponse(request, 'home.html', ctx)
