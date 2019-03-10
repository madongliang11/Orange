# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.account import views

urlpatterns = [
    url('login/', views.login_view, name='login'),
    url('register', views.register, name='register'),
    url('update/', views.update),
    url('logout/', views.logout_view, name='logout'),
    url('active/',views.active_account),
]
