from django.contrib import admin
from django.urls import path
from .views import webhook,stop_container,start_container

urlpatterns = [
    path('webhook/',webhook,name='webhook'),
    path('start_container/',start_container,name='start_container'),
    path('stop_container/',stop_container,name='stop_container')
]