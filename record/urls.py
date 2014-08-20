from django.conf.urls import patterns, url

from record import views

urlpatterns = patterns('',
                       url(r'^$',views.spendingView, name='spending')
                       )
