#coding=utf-8

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.util import ErrorList

class LoginForm(AuthenticationForm):
    username = forms.CharField(error_messages = {'required': u'用户名或邮箱不能为空'}, max_length = 30)
    password = forms.CharField(widget=forms.PasswordInput, error_messages = {'required': u'密码不能为空'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username = username, password = password)
            if self.user_cache is None:
                #尝试用Email登录
                try:
                   User.objects.get(email = username).username
                except:
                    raise forms.ValidationError("请输入正确的用户名、密码")
                else:
                    username_from_email = User.objects.get(email = username).username
                    
                self.user_cache = authenticate(username = username_from_email, password = password)
                    
                #临时密码登录
                #user_temp_pwd_list = AccountTempPassword.objects.filter(temp_password = password, user__username = username)
                #if user_temp_pwd_list:
                #    user = user_temp_pwd_list[0].user
                    #login(self.request, user)
                #    self.request.session['temp_login'] = user
                    
                    #删除临时密码
                #    for user_temp_pwd in user_temp_pwd_list:
                #        user_temp_pwd.delete()
                        
                #    raise forms.ValidationError("")
                #else:
                
                
        self.check_for_test_cookie()
        return self.cleaned_data

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, error_messages = {'required': u'密码不能为空', 'min_length':u'至少是6个字符', 'max_length':u'最多是16个字符'}, min_length = 6, max_length = 16)
    confirm_password = forms.CharField(widget=forms.PasswordInput, error_messages = {'required': u'确认密码不能为空', 'min_length':u'至少是6个字符', 'max_length':u'最多是16个字符'}, max_length = 16)
    identifier = forms.CharField()
    
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email = email).count() > 0
        if exists:
            raise forms.ValidationError(u'邮箱已经被使用，请更换邮箱')
        return email
        
    def clean_username(self):
        username = self.cleaned_data['username']
        exists = User.objects.filter(username = username).count() > 0
        if exists:
            raise forms.ValidationError(u'该用户名已被使用，请重新输入')
#        if username[0].isdigit():
#            raise forms.ValidationError(u'用户名不能以数字开头')
        return username
    
    def clean(self):
        if ('confirm_password' in self.cleaned_data) and ('password' in self.cleaned_data):
            if (self.cleaned_data['confirm_password'] != self.cleaned_data['password']):
                self._errors["confirm_password"] = ErrorList([u'密码与确认密码不匹配'])
                del self.cleaned_data['password']
                del self.cleaned_data['confirm_password']
                
        return self.cleaned_data
