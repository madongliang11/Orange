# -*- coding: utf-8 -*-
from django.conf.urls import url


from apps.detail import views

urlpatterns = [
    url('info/',views.detail,name='detail'),
]
