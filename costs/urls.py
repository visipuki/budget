from django.conf.urls import patterns, url

from costs import views

urlpatterns = patterns('',
                       url(r'^$', views.spendingView, name='index')
                       )
