from django.conf.urls import patterns, url
from analytics import views


urlpatterns = patterns('',
                       url(r'^$', views.analyticsView),
                       url(r'^(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{4})/$',
                           views.analyticsView))
