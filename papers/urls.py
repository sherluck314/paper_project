from django.conf.urls import url

from . import views
from django.urls import path

app_name = 'papers'

urlpatterns = [
    path('index', views.index, name="index"),
    path('', views.show, name="show"),
    path('content/<int:pk>/', views.detail, name='detail'),
    path('<str:keyword>=<str:value>/', views.filter_by_keyword, name='filter_by_keyword'),
    path('search/<str:keywords>', views.filter_by_keywords, name='filter_by_keywords')
]