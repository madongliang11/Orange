# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy


class OrangemallCategory(scrapy.Item):
    #分类id
    cate_id = scrapy.Field()
    #上一级分类id
    parent_id = scrapy.Field()
    #分类级别
    level = scrapy.Field()
    #商品名称
    name = scrapy.Field()
    #创建时间
    create_time = scrapy.Field()
    #状态
    is_delete = scrapy.Field()

    def get_name(self):
        return OrangemallCategory.__name__


class OrangemallShop(scrapy.Item):
    #商品id
    shop_id = scrapy.Field()
    #商品名称
    name = scrapy.Field()
    #商品原价
    original_price = scrapy.Field()
    #商品折扣价
    promote_price = scrapy.Field()
    #库存
    stock = scrapy.Field()
    #外键 商品分类
    cate_id = scrapy.Field()
    #创建时间
    create_date = scrapy.Field()
    sale = scrapy.Field()
    sort = scrapy.Field()
    #是否热卖
    is_hot = scrapy.Field()
    #状态
    is_delete = scrapy.Field()

    def get_name(self):
        return OrangemallShop.__name__

class OrangeMallProperty(scrapy.Item):
    property_id = scrapy.Field()
    name = scrapy.Field()
    shop_id = scrapy.Field()
    is_delete = scrapy.Field()

    def get_name(self):
        return OrangeMallProperty.__name__

class OrangeMallImage(scrapy.Item):
    #图片id
    img_id = scrapy.Field()
    #外键 商品id
    shop_id = scrapy.Field()
    #图片类型
    type = scrapy.Field()
    #图片地址
    img_url = scrapy.Field()
    #状态
    is_delete = scrapy.Field()

    def get_name(self):
        return OrangeMallImage.__name__

class DownloadImg(scrapy.Item):
    download_img = scrapy.Field()

    def get_name(self):
        return DownloadImg.__name__

