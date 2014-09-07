from django.conf.urls import patterns, url
from transfer import views


urlpatterns = patterns('',
                       url(r'^$', views.transferView),
                       url(r'^(\d+)/$', views.transferView))
