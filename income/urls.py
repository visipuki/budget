from django.conf.urls import patterns, url
from income import views


urlpatterns = patterns('',
                       url(r'^$', views.incomeView),
                       url(r'^(\d+)/$', views.incomeView))
