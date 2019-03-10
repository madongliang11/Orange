# -*- coding: utf-8 -*-
import random

import scrapy
import time
from scrapy import Request

from db.models import synchronous
from items import OrangemallCategory
from utils.bshead import create_bs_driver
(minst, session) = synchronous()

def myrandom():
    return random.randint(100000,999999)

class MunescrapySpider(scrapy.Spider):
    name = 'munescrapy'
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
            r = Request(url=url,dont_filter=True,meta={'type':'move_out'},callback=self.parse_list)
            yield r

    def parse_list(self,response):
        first_list = response.xpath("//ul[@class='JS_navCtn cate_menu']/li")
        i=1
        for li in first_list:
            # 一级菜单
            name1 = li.xpath("./a/text()").extract()
            str = ''
            for n in name1:
                str = str+' '+n
            name1_id = myrandom()
            cate1 = OrangemallCategory(cate_id=name1_id,parent_id=0,level=1,name=str,create_time=time.time(),is_delete=0)
            yield cate1
            j=1
            try:
                # 二级菜单
                name2 = response.xpath(
                    f"//div[@id='J_popCtn']/div[{i}]/div[1]/div[2]/dl[@class='cate_detail_item cate_detail_item{j}']/dt/a/text()").extract_first()
                dls = response.xpath(f"//div[@id='J_popCtn']/div[{i}]/div[1]/div[2]/dl")
                for dl in dls:
                    name2 = dl.xpath("./dt/a/text()").extract()
                    name2_id = myrandom()
                    cate2 = OrangemallCategory(cate_id=name2_id, parent_id=name1_id, level=2, name=name2,
                                              create_time=time.time(), is_delete=0)
                    yield cate2
                    dds = dl.xpath("./dd/a")
                    for dd in dds:
                        name3 = dd.xpath("./text()").extract()
                        name3_id = myrandom()
                        cate3 = OrangemallCategory(cate_id=name3_id, parent_id=name2_id, level=3, name=name3,
                                                       create_time=time.time(), is_delete=0)
                        yield cate3



            except Exception as e:
                print(e)

            i += 1
