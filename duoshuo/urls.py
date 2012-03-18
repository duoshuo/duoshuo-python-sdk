from django.conf.urls.defaults import patterns, url

from duoshuo import views as duoshuo_views

urlpatterns = patterns('',
    url(r'^login/$',
       duoshuo_views.login,
       name='duoshuo_login'),
    url(r'^register/$',
       duoshuo_views.register,
       name='duoshuo_register'),
)
