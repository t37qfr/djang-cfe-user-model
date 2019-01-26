from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from accounts.views import register, user_login, home, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^register/$', register),
    url(r'^login/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^$', home),
]
