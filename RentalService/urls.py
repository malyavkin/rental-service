from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from DocXTools import urls as app_urls

urlpatterns = [
    url(r'^', include(app_urls)),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]


