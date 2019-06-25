from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from haystack.views import SearchView
from apps.main.models import Image

from apps.main.models import Category, Headline, Banner, ShopCar, Shop

def index(request):
    head_list = Headline.objects.all()
    banner_list = Banner.objects.all()
    hot_list = Shop.objects.filter(is_hot=0)[:4]
    for hot_shop in hot_list:
        hot_shop.image = hot_shop.image_set.filter(type='big').first()
    cate_list = Category.objects.filter(level=1)
    # shop_car_queryset = ShopCar.objects.filter(shop_id=request.user.id)
    # shop_car_num = shop_car_queryset.count() if shop_car_queryset.exists() else 0
    for cate in cate_list:
        sub_menus = Category.objects.filter(parent_id=cate.cate_id, level=2)
        for sub_menu in sub_menus:
            sub_menus2 = Category.objects.filter(parent_id=sub_menu.cate_id, level=3)
            sub_menu.sub_menus2 = sub_menus2
        cate.sub_menus = sub_menus

    sub_cates = Category.objects.filter(level=3)[:30]
    sub_list = []
    for sub_cate in sub_cates:
        shops = sub_cate.shop_set.all()
        if len(shops):
            sub_list.append(sub_cate)
            for shop in shops:
                shop.image = shop.image_set.all().first()
            sub_cate.shops = shops

    return render(request, 'index.html', locals())



def car_shop_num(request):
    car_num = 0
    uid = request.user.id
    shops_car=ShopCar.objects.filter(user=uid,status=1).all()
    for shop_car in shops_car:
        car_num += shop_car.number
    data = {
        'car_num':car_num
    }
    result ={'status':200,'msg':'ok','data':data}

    return JsonResponse(result)
    # return render(request,'./common/top.html',locals())


class MySearchView(SearchView):
    def create_response(self):
        context = self.get_context()
        shops = context['page']
        for shop in shops:
            shop.object.img_url = Image.objects.filter(shop_id=shop.object.shop_id,type='big').values('img_url').first()['img_url']
            # shop.object.img_url = shop.image_set.img_url[0]
        context['page'] = shops
        return render(self.request, self.template, context)




