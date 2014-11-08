from django.conf.urls import patterns, url

from debt import views

urlpatterns = patterns(
    '',
    url(r'^$', views.debtView),
    url(r'^(\d+)/$', views.debtView),
)
