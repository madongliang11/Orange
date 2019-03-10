from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django_ajax.decorators import ajax

from apps.main.models import ShopCar, Address, Area, Order


@login_required
def confirm1(request):
    oid = request.GET.get('oid')
    shops = ShopCar.objects.filter(order_id=oid)
    return render(request, 'confirm.html', {'shops': shops})


def payment(request):
    oid = request.GET.get('oid')
    # shops = ShopCar.objects.filter(order_id=oid)
    id = request.user.id
    # 获取用户默认地址
    # 字段status表示用户地址的状态，0：正常，1：默认地址
    defaultaddr = Address.objects.filter(user=id,is_detele=False,status=1).first()
    # 获取用户地址
    address = Address.objects.filter(user=id,is_detele=False,status=0)
    # 获取用户购物车列表
    cars = ShopCar.objects.filter(order_id=oid, status=1)
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
    # 获取所有地区的省级名称
    provinces = Area.objects.filter(level=1)
    # citys = Area.objects.filter(level=2)
    # areas = Area.objects.filter(level=3)
    return render(request, 'order.html', locals())


def setdefault(request):
    if request.method == 'GET':
        aid = request.GET.get('aid')
        uid = request.user.id
        # 将原来的默认地址修改为非默认地址
        address = Address.objects.filter(user=uid,is_detele=False,status=1)
        if address:
            for addr in address:
                addr.status=0
                addr.save()
        # 设置新的默认地址
        addr = Address.objects.filter(aid=aid,is_detele=False)
        if addr.exists():
            addr.update(status=1)
    else:
        return HttpResponse('不支持的请求方式')

# 根据省筛选市
@ajax
def select_addr(request):
    if request.method == 'GET':
        province_name = request.GET.get('province')
        if province_name:
            province = Area.objects.filter(name=province_name).first()
            citys = Area.objects.filter(parent_id=province.aid)
            city_list = []
            for city in citys:
                city_list.append(city)
            return {'citys':city_list}
    else:
        return HttpResponse('不支持的请求方式')

# 根据市筛选区
@ajax
def select_city(request):
    if request.method == 'GET':
        city_name = request.GET.get('city')
        if city_name:
            city = Area.objects.filter(name=city_name).first()
            dists = Area.objects.filter(parent_id=city.aid)
            dist_list = []
            for dist in dists:
                dist_list.append(dist)
            return {'dists':dists}
    else:
        return HttpResponse('不支持的请求方式')





# 删除地址
def deladdr(request):
    if request.method=='GET':
        aid = request.GET.get('aid')
        addr = Address.objects.filter(aid=aid)
        if addr.exists():
            addr.update(is_detele=True)
            # return HttpResponse('Ok')
    else:
        return HttpResponse('不支持的请求方式')

@ajax
def add_addr(request):
    if request.method=='POST':
        reciver = request.POST.get('name')
        phone = request.POST.get('phone')
        province = request.POST.get('province')
        city = request.POST.get('city')
        area = request.POST.get('dist')
        detail_loc = request.POST.get('detail')
        if reciver and phone and province and city and area and detail_loc:
            address = Address(reciver=reciver,phone=phone,province=province,city=city,area=area,detail_loc=detail_loc,status=0,is_detele=False,user=request.user)
            address.save()
            return {'msg':'OK','reciver':reciver,'phone':phone,'province':province,'city':city,'dist':area,'street':detail_loc,'aid':address.aid}
        else:
            return {'msg':'error'}
    else:
        return HttpResponse('不支持的请求方式')

def pay_success(request):
    if request.method == 'GET':
        order_code = request.GET.get('order_code')
        aid = request.GET.get('aid')
        address = Address.objects.filter(aid=aid).first()
        amount = request.GET.get('total')
        if order_code:
            order = Order.objects.filter(order_code=order_code)
            if order:
                order.update(status=0)
            car_shops = ShopCar.objects.filter(order=order.first().oid).all()
            for car_shop in car_shops:
                car_shop.status = 0
                car_shop.save()
    return render(request,'pay_success.html',locals())




