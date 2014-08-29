from django.conf.urls import patterns, url

from costs import views

urlpatterns = patterns('',
                       url(r'^$', views.spendingView),
                       url(r'^(\d+)/$', views.spendingView),
                       )
