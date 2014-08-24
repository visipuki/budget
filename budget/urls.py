from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from costs.views import spendingView
from income.views import incomeView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'budget.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', spendingView),
                       url(r'^analytics/', include('analytics.urls')),
                       url(r'^income/$', incomeView),
                       url(r'^accounts/login/$', auth_views.login),
                       url(r'^accounts/logout/$', auth_views.logout_then_login),
)
