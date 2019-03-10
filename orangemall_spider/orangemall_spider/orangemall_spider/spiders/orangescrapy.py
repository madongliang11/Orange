# -*- coding: utf-8 -*-
import hashlib
import random
import time

import re
import scrapy
from scrapy import Request

from db.models import synchronous, Category
from items import OrangeMallProperty, OrangemallShop, OrangeMallImage, DownloadImg
from utils.bshead import create_bs_driver

(minst, session) = synchronous()

def create_fingerprint(url, type="md5"):
    minst = hashlib.md5() if type == "md5" else hashlib.sha1()
    minst.update(url.encode("utf8"))
    return minst.hexdigest()


class OrangescrapySpider(scrapy.Spider):
    name = 'orangescrapy'
    allowed_domains = ['jd.com']
    start_urls = ['http://www.jd.com/']

    def __init__(self):
        scrapy.Spider.__init__(self,self.name)
        self.driver = create_bs_driver()
        self.driver.set_page_load_timeout(20)

    def __del__(self):
        self.driver.quit()

    def start_requests(self):
        for url in self.start_urls:
            r = Request(url=url, callback=self.parse,dont_filter=True,meta={"type":"move_out"})
            yield r

    def parse(self,response):
        # 一级菜单节点
        first_list = response.xpath("//ul[@class='JS_navCtn cate_menu']/li")
        i=1
        for li in first_list:
            # name1 = li.xpath("./a/text()").extract()
            j=1
            try:
                # 二级菜单节点
                dls = response.xpath(f"//div[@id='J_popCtn']/div[{i}]/div[1]/div[2]/dl")
                for dl in dls:
                    # name2 = dl.xpath("./dt/a/text()").extract()
                    dds = dl.xpath("./dd/a")
                    for dd in dds:
                        name3 = dd.xpath("./text()").extract_first()
                        note = minst.query_conditions(session,Category,Category.name,name3).first()
                        if note:
                            url = dd.xpath("./@href").extract_first()
                            url=f"https:{url}"
                            r = Request(url=url,dont_filter=True,callback=self.parse_page,meta={"type":"cate_page"})
                            yield r
                            break

            except Exception as e:
                print(e)

            i += 1

    def parse_page(self,response):
        list = response.xpath("//ul[@class='gl-warp clearfix']/li/div/div[@class='p-img']/a")
        if list:
            url = list.xpath("./@href").extract_first()
            url = f"https:{url}"
            r = Request(url=url,dont_filter=True,callback=self.parse_detail,meta={"type":"detail"})
            yield r

    def parse_detail(self,response):
        # 分类id
        cate_name = response.xpath("//div[@class='crumb fl clearfix']/div[5]/a/text()").extract_first()
        r = minst.query_conditions(session, Category, Category.name, cate_name).first()

        if r:
            cate_id = r.cate_id

            # 获取商品信息
            # 商品ID

            shop_id = int(random.randint(1000000, 9999999))
            # 商品名字
            name = response.xpath("//div[@class='sku-name']/text()").extract()
            name = "".join(name).strip()
            # 商品原价
            original_price = response.xpath("//span[@class='p-price']/span[2]/text()").extract_first()
            # 商品折扣价
            promote_price = '1000.00'
            # 商品库存
            stock = 10000
            # 外键 cate
            cate_id = cate_id
            shop_item = OrangemallShop(shop_id=shop_id, name=name, original_price=original_price,
                                       promote_price=promote_price, stock=stock, cate_id=cate_id, create_date=time.time(),
                                       sale=2000,sort=2000,is_hot=1, is_delete=0)
            yield shop_item

            # 获取商品详细数据
            list = response.xpath("//ul[@class='parameter2 p-parameter-list']/li/text()").extract()
            for li in list:
                property_li = OrangeMallProperty(property_id=random.randint(100000, 999999), name=li, shop_id=shop_id,
                                                 is_delete=0)
                yield property_li

            # 获取商品的图片
            list = response.xpath("//ul[@class='lh']/li")
            for li in list:
                img = li.xpath("./img/@src").extract_first()
                small_img = f'https:{img}'

                # 处理详情页图片的尺寸问题
                p = re.compile(r"s\d{2}x\d{2}_jfs")
                str1 = p.search(small_img)
                if str1:
                    big_img = small_img.replace(str1.group(), 's450x450_jfs')
                else:
                    big_img = small_img.replace('n5', 'n1')

                # 下载图片
                download_img = DownloadImg(download_img=big_img)
                yield download_img

                img_item = OrangeMallImage(img_id=random.randint(100000, 999999), shop_id=shop_id, type='small',
                                           img_url=create_fingerprint(big_img), is_delete=0)
                yield img_item

                img_item = OrangeMallImage(img_id=random.randint(100000, 999999), shop_id=shop_id, type='big',
                                           img_url=create_fingerprint(big_img), is_delete=0)
                yield img_item

