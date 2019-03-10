# -*- coding: utf-8 -*-
__authon__ = 'lp'
__date__ = '2019/1/20 17:03'


'''
图片下载
'''
import scrapy

from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		image_url = item.get('download_img', None)
		if image_url != None:
			yield scrapy.Request(url=image_url)