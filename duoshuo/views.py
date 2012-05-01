# -*- coding: utf-8 -*-
import urlparse

from django.db.transaction import commit_on_success
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from duoshuo import DuoshuoAPI
from duoshuo.models import Auth
from duoshuo.forms import RegistrationForm

ds = DuoshuoAPI()

@csrf_protect
@never_cache
def duoshuo_login(request, template_name='duoshuo/login.html',
          redirect_field_name=None,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    oauth_url = ds.get_url(redirect_uri='http://127.0.0.1:8007/login/')
    code = request.GET.get('code','')
    
    if request.method == "POST":
        form = authentication_form(request=request, data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            # 登录后把多说identifier存入数据表
            identifier = request.POST.get('identifier')
            print identifier
            Auth.objects.create(user=form.get_user(),identifier=identifier)
            
            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        if code:
            identifier = ds.get_token(code).get('user_id')
            if identifier:
                try:
                    ds_user = Auth.objects.get(identifier=identifier)
                except:
                    # 如果用户还没有绑定多说帐号，让他登录或是注册
                    context = {
                        'form' : authentication_form(request),
                        'register_form' : RegistrationForm(), 
                        'oauth_url' : oauth_url,
                        'identifier' : identifier
                    }
                    return render_to_response(template_name, context,
                                  context_instance=RequestContext(request, current_app=current_app))
                else:
                    # 已经绑定多说帐号则直接登录网站
                    user = ds_user.user
                    user.backend='django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return redirect('/accounts/profile/')
            else:
                #无效的code，将code从查询字符串中去掉
                query = QueryDict(request.META.get('QUERY_STRING'))
                query_string = query.copy()
                query_string.pop('code')
                return redirect( '%s?%s' % (request.META.get('PATH_INFO'), query_string.urlencode()) )
        
        redirect_to = request.REQUEST.get(redirect_field_name, '')
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)
    
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'oauth_url': oauth_url,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))

@csrf_protect
@commit_on_success
def duoshuo_register(request):
    oauth_url = ds.get_url(redirect_uri='http://127.0.0.1:8007/login/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]
            identifier = form.cleaned_data["identifier"]
            user = User.objects.create_user(username = username, email = email, password = password)
            Auth.objects.create(user=user, identifier=identifier)
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('/accounts/profile/')
        else:
            return redirect('/accounts/profile/')
    else:
        code = request.GET.get('code','')
        if code:
            identifier = ds.get_token(code).get('user_id')
            print identifier
            if identifier:
                try:
                    ds_user = Auth.objects.get(identifier=identifier)
                except:
                    context = {
                        'oauth_url' : oauth_url,
                        'identifier' : identifier,
                        'form' : RegistrationForm(initial={'identifier': identifier}), 
                    }
                    return render_to_response('duoshuo/register.html', context,
                                              context_instance=RequestContext(request))
                else:
                    pass
                
                    
        context = {
            'oauth_url' : oauth_url,
            'form' : RegistrationForm(), 
        }
        return render_to_response('register.html', context,
                                  context_instance=RequestContext(request))

def callback(request):
    duoshuo_code = request.GET.get('code','')
    if duoshuo_code:
        ds = DuoshuoAPI()
        response = ds.get_token(code=duoshuo_code)
        request.session['access_token'] = response['access_token']
        duoshuo_id = response['user_id']
        binding = UserProfile.objects.filter(duoshuo_id=duoshuo_id).count()
        if binding:
            userprofile = UserProfile.objects.get(duoshuo_id=duoshuo_id)
            user = userprofile.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            if request.user.id:
                userprofile = request.user.get_profile()
                userprofile.duoshuo_id = response['user_id']
                userprofile.save()
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')