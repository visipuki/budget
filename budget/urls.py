from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'budget.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('spending.urls')),
                       url(r'^analytics/', include('analytics.urls')),
                       url(r'^income/', include('income.urls')),
                       url(r'^transfer/', include('transfer.urls')),
                       url(r'^debt/', include('debt.urls')),
                       url(r'^accounts/login/$', auth_views.login),
                       url(r'^accounts/logout/$', auth_views.logout_then_login),
)
