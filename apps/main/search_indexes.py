# -*- coding :utf-8 -*-
__author__ = 'peiming'
__date__ = '2019/2/12 0012 17:16'

from haystack import indexes
from apps.main.models import Shop

#指定对于电影类的某些数据建立索引
# 注意:类名必须为要检索的Model_Name+Index
# 据模板的路径为templates/search/indexes/yourapp/note_text.txt
# note_text.txt文件名必须为要索引的类名_text.txt

class ShopIndex(indexes.SearchIndex,indexes.Indexable):
    # 创建一个text字段
    text = indexes.CharField(document=True,use_template=True)

    # 重载方法
    def get_model(self):
        return Shop

    def index_queryset(self,using=None):
        result = self.get_model().objects.all()
        return result







