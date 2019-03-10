# -*- coding：utf-8 -*-
__author__ = 'madl'
__date__ = '2019/1/25 0025 上午 11:39'

from django.conf.urls import url
from apps.order import views


urlpatterns = [
    url('payment/',views.payment,name='payment'),
    url('setdefault/',views.setdefault,name='setdefault'),
    url('deladdr/',views.deladdr,name='deladdr'),
    url('add_addr/',views.add_addr,name='add_addr'),
    url('select/',views.select_addr,name='select'),
    url('selcity/',views.select_city,name='selcity'),
    url('success/',views.pay_success,name='pay_sucess')
]