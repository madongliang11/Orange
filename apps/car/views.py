import datetime
import json
import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_ajax.decorators import ajax

from apps.main.models import ShopCar, Order, User


@login_required
def car_list(request):
    if request.method=='GET':
        id = request.user.id
        # 获取用户购物车列表
        cars = ShopCar.objects.filter(user=request.user.id, status=1)
        total_price = 0
        shop_num = 0
        for car in cars:
            # 商品图片
            car.image = car.shop.image_set.filter(shop_id=car.shop.shop_id).first()
            # 商品总价
            car.sum_price = float(car.shop.promote_price) * car.number
            total_price += car.sum_price
            shop_num += car.number
            car.shop_name = car.shop.name[:6]
        return render(request, 'car.html', context={'cars': cars, 'total_price': total_price, 'shop_num': shop_num})


def del_shop(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        if car_id:
            # 如果购物车存在，购物车status改为0
            car = ShopCar.objects.filter(car_id=car_id)
            if car.exists():
                car.update(status=0)
    else:
        return HttpResponse('不支持的请求方式')


@ajax
@login_required
def confirm(request):
    if request.method == 'POST':
        car_str = request.POST.get('car')
        if car_str:
            cars = json.loads(car_str)
            try:
                # 开启事物
                with transaction.atomic():
                    # 生成订单
                    oid = product_order(request).oid
                    # oid = 1
                    for car in cars:
                        car_id = car.get('car_id')
                        num = car.get('num')
                        ShopCar.objects.filter(car_id=car_id).update(number=num, order_id=oid)
                return {'oid': oid}
            except Exception as e:
                print(e)
                transaction.rollback()
        else:
            pass


# 生成订单信息
def product_order(request):
    # 第一步生成订单号  全站必须唯一   尽量大于8位
    order_code = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100000,999999)}"
    order = Order(order_code=order_code, user=request.user)
    if order:
        order.save()
        return order
    else:
        print('错误')


#完成支付后，将订单和购物车中商品的状态进行更新
def update_order(request):
    if request.method=='POST':
        order_code = request.GET.get('order_code')
        order = Order.objects.first(order_code=order_code)
        if order:
            order.update(status=0)
        car_shops =ShopCar.objects.filter(oid=order.first().oid)
        for car_shop in car_shops:
            car_shop.update(status=0)
    return render(request,'car.html')
