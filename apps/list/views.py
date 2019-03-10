import random

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from apps.main.models import Shop, Image, Category,User


def list_all(request):
    cate_1 = Category.objects.filter(level=1).values('name', 'cate_id')
    # cate_1 = random.sample(list(cate_1),8)
    # cate_2 = Category.objects.filter(level=3).values('name')
    # cate_2 = random.sample(list(cate_2), 8)
    # cate_3 = Shop.objects.all().values('name')
    # cate_3 = random.sample(list(cate_3),5)
    shops = Shop.objects.all().values('name', 'original_price', 'sale', 'shop_id')
    shop_numbers = Shop.objects.all().count()
    i = 0
    price = '0'
    sale_num = None
    price_sort = None
    # 根据价格筛选
    # 0代表全部 1代表0~100 2代表100~200 3代表200~500 4代表500+
    price = request.GET.get('price', '0')
    if price != '0':
        if price == '1':
            shops = shops.filter(original_price__gte=0, original_price__lt=100)
        elif price == '2':
            shops = shops.filter(original_price__gte=100, original_price__lt=200)
        elif price == '3':
            shops = shops.filter(original_price__gte=200, original_price__lt=500)
        elif price == '4':
            shops = shops.filter(original_price__gte=500)

    #销量排序
    sale_num = request.GET.get('sale_num')
    if sale_num == '1':
        shops = shops.order_by('-sale')
    elif sale_num == '2':
        shops = shops.order_by('sale')

    #价格排序
    price_sort = request.GET.get('price_sort')
    if price_sort == '1':
        shops = shops.order_by('-original_price')
    elif price_sort == '2':
        shops = shops.order_by('original_price')
    for shop in shops:
        img = Image.objects.filter(shop_id=shop.get('shop_id')).values('img_url').first()
        shop['img_url'] = img['img_url']
        i +=1

        # 分页功能

        paginator = Paginator(shops, 20)
        page = request.GET.get('page')
        if page:
            page = int(page)
        else:
            page = 1
        if page > paginator.num_pages:
            page = 1
        shop_list = paginator.page(page)
        num_pages = paginator.num_pages
        if num_pages < 5:
            # 1-num_pages
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            # num_pages-4, num_pages
            pages = range(num_pages - 4, num_pages + 1)
        else:
            # page-2, page+2
            pages = range(page - 2, page + 3)
    return render(request, 'list.html', locals())


def sort(request):
    cate_1 = Category.objects.filter(level=1).values('name', 'cate_id')
    cate_id = request.GET.get('cate_id')
    # cate_2 = Category.objects.filter(parent_id=cate_id).values('cate_id')
    # for i in cate_2:
    #     cate_3 = Category.objects.filter(parent_id=i['cate_id']).values('cate_id')
    #     for i in cate_3:
    #         shops = Shop.objects.filter(cate_id=i['cate_id']).values('name', 'original_price', 'sale', 'shop_id')

    shops = Shop.objects.filter(cate_id=cate_id)
    i = 0
    if shops:

        price = '0'
        sale_num = None
        price_sort = None
        # 根据价格筛选
        # 0代表全部 1代表0~100 2代表100~200 3代表200~500 4代表500+
        price = request.GET.get('price', '0')
        if price != '0':
            if price == '1':
                shops = shops.filter(original_price__gte=0, original_price__lt=100)
            elif price == '2':
                shops = shops.filter(original_price__gte=100, original_price__lt=200)
            elif price == '3':
                shops = shops.filter(original_price__gte=200, original_price__lt=500)
            elif price == '4':
                shops = shops.filter(original_price__gte=500)

        # 销量排序
        sale_num = request.GET.get('sale_num')
        if sale_num == '1':
            shops = shops.order_by('-sale')
        elif sale_num == '2':
            shops = shops.order_by('sale')
        # 价格排序
        price_sort = request.GET.get('price_sort')
        if price_sort == '1':
            shops = shops.order_by('-original_price')
        elif price_sort == '2':
            shops = shops.order_by('original_price')
        for shop in shops:
            img = Image.objects.filter(shop_id=shop.shop_id).values('img_url').first()
            shop.img_url = img['img_url']
            i += 1
        # for shop in shops:
        #     img = Image.objects.filter(shop_id=shop.get('shop_id')).values('img_url').first()
        #     shop['img_url'] = img['img_url']
            # 分页功能
            paginator = Paginator(shops, 20)
            page = request.GET.get('page')
            if page:
                page = int(page)
            else:
                page = 1
            if page > paginator.num_pages:
                page = 1
            shop_list = paginator.page(page)
            num_pages = paginator.num_pages
            if num_pages < 5:
                # 1-num_pages
                pages = range(1, num_pages + 1)
            elif page <= 3:
                pages = range(1, 6)
            elif num_pages - page <= 2:
                # num_pages-4, num_pages
                pages = range(num_pages - 4, num_pages + 1)
            else:
                # page-2, page+2
                pages = range(page - 2, page + 3)

        return render(request, 'sort.html', locals())

    else:
        return redirect(reverse('list:all'))





