from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns('accounts.views',
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^register/$', 'register'),
    url(r'^callback/$', 'callback'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
)
