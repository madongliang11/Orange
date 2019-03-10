# -*- coding: utf-8 -*-  




from db.models import synchronous, Category, Shop, Property, Image

(minst, session) = synchronous()


#
# BOOK_ITEM_MAP = {
# 	'BooktoscrapeItem':(Book, ('book_title', 'image_url', 'book_url', 'book_url_fprint', 'book_price')),
#     'BookDetailItem':(BookDetail, ('book_url_fprint', 'book_description')),
# }


class SyncMySQLBookPipeLine(object):

    def process_item(self, item, spider):
        '''
        :param item:  item是从spiders通过yield发射过来的对象
        :param spider:  spider是指的不同爬虫 （spider.name）
        :return:
        '''
        try:
            item_name = item.get_name()
            if item_name == "OrangemallCategory":
                cate = Category(cate_id=item['cate_id'], parent_id=item['parent_id'], level=item['level'], name=item['name'], create_time=item['create_time'], is_delete=item['is_delete'])
                minst.add_records(session, cate)

            elif item_name == "OrangemallShop":
                shop = Shop(shop_id=item['shop_id'], name=item['name'], original_price=item['original_price'], promote_price=item['promote_price'], stock=item['stock'],
                cate_id=item['cate_id'], create_date=item['create_date'], sale=item['sale'], sort=item['sort'], is_hot=item['is_hot'], is_delete=item['is_delete'])
                minst.add_records(session, shop)

            elif item_name == "OrangeMallProperty":
                property = Property(property_id=item['property_id'], name=item['name'], shop_id=item['shop_id'], is_delete=item['is_delete'])
                minst.add_records(session, property)

            elif item_name == "OrangeMallImage":
                image = Image(img_id=item['img_id'], shop_id=item['shop_id'], type=item['type'], img_url=item['img_url'],is_delete=item['is_delete'])
                minst.add_records(session, image)

        # return item
        except Exception as e:
            print(f"MySQLBookPipeLine:process_item has error: {e}")
        # return item
        finally:
            return item
