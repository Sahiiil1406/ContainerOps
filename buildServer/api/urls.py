from django.contrib import admin
from django.urls import path, include
from . import views

app_name="api"
urlpatterns = [
    
    path('signup/', views.create_user, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('fetch_giturl/', views.fetch_giturl, name='fetch_giturl'),
    path('deploy/', views.run, name='deploy'),

    #frontend pages
    path('frontend/', views.landing_page, name='landing_page'),
    path('frontend/deploy/', views.deploy_page, name='deploy_page'),
    path('frontend/list/', views.list_page, name='list_page'),
]
