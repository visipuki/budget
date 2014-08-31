from django.conf.urls import patterns, url

from spending import views

urlpatterns = patterns('',
                       url(r'^$', views.spendingView),
                       url(r'^(\d+)/$', views.spendingView),
                       )
