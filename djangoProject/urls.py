from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^papers/', include('papers.urls')),
    url(r'^admin/', admin.site.urls),
]