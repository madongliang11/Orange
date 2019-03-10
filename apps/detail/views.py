from django.db.models import F
from django.shortcuts import render

from apps.main.models import Image, Shop, Property, Category, ShopCar, User


# Create your views here.


def detail(request):
    if request.method == 'GET':
        user  = request.user
        shop_id = request.GET.get("id")
        shop_id = int(shop_id)
        # #商品图片列表
        r = Image.objects.filter(shop_id=shop_id).values("img_url")
        imgs = [img for img in r][:4]
        imgs_first = imgs[0].get("img_url")
        # 商品对象
        shop = Shop.objects.filter(shop_id=shop_id)
        original_price = shop.first().original_price
        promote_price = shop.first().promote_price
        # 商品属性
        property = Property.objects.filter(shop_id=shop_id).all()
        #分类
        cate3 = Category.objects.filter(cate_id=shop.values("cate_id"))
        cate_name3 = cate3.first().name
        return render(request, 'detail.html', locals())

    elif request.method == 'POST':
        result = {'status': 200, 'msg': '添加成功！'}
        #将用户选中的商品加入购物车
        shop_id = request.POST.get('shop_id')
        shop_num = request.POST.get('shop_num')
        uid = request.user.id
        shop = Shop.objects.filter(shop_id=shop_id).first()

        user = User.objects.filter(id=uid).first()
        car_shops = ShopCar.objects.filter(shop=shop_id,status=1,user=request.user.id)
        if car_shops.exists() :
            car_shops.update(number=F('number') + int(shop_num))
        else:
            car_shop = ShopCar(shop=shop, user=user, number=shop_num)
            car_shop.save()
        return result

        # if car_shop and car_shop.first().status==1:
        #     car_shop.update(number=F('number')+int(shop_num))
        # else:
        #     car_shop = ShopCar(shop=shop, user=user, number=shop_num)
        #     car_shop.save()
        #     # update_number = update_number if  update_number else False
        # # result.update(data=update_number)
        # return result
    else:
        msg = '商品不存在或已下架！'
        result = {'status':400,'msg':msg}








