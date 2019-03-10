# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.main import views

urlpatterns = [
    url('car_shop_num/', views.car_shop_num, name='car_shop_num'),

]
