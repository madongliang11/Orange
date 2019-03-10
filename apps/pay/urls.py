# -*- coding: utf-8 -*-
from django.conf.urls import url


from apps.pay import views

urlpatterns = [
    url('pay/',views.our_pay,name='pay'),
]
