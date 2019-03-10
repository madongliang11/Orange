# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/12/19 上午9:59'

'''
自定义orm业务模型类
'''



from sqlalchemy import Column, String, Integer, ForeignKey

from db.mysql_helper import MySQLORMHelper, Base


class Category(Base):
    __tablename__ = "category"
    cate_id = Column(Integer, primary_key=True)  # db can set it auto_increment
    parent_id = Column(Integer)
    level = Column(Integer)
    name = Column(String(255))
    create_time = Column(String(100))
    is_delete = Column(Integer)




class Shop(Base):
    __tablename__ = "shop"
    shop_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    original_price = Column(String(20))
    promote_price = Column(String(20))
    stock = Column(Integer)
    cate_id = Column(Integer, ForeignKey(Category.cate_id))
    create_date = Column(String(100))
    sale = Column(Integer)
    sort = Column(Integer)
    is_hot = Column(Integer)
    is_delete = Column(Integer)


class Property(Base):
    __tablename__ = "property"
    property_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(64))
    shop_id = Column(Integer,ForeignKey(Shop.shop_id))
    is_delete = Column(Integer)


class Image(Base):
    __tablename__ ="image"
    img_id = Column(Integer,primary_key=True,autoincrement=True)
    shop_id = Column(Integer,ForeignKey(Shop.shop_id))
    type = Column(String(32))
    img_url = Column(String(255))
    is_delete = Column(Integer)

def synchronous():
    minst = MySQLORMHelper()
    session = minst.create_session()
    return (minst, session)


if __name__ == "__main__":
    synchronous()
    # (minst, session) = synchronous()
    # cate_name =  '洗衣机'
    # r = session.query(Category).filter(Category.name == cate_name).first()
    # #r = minst.query_conditions(session, Category, Category.name, cate_name)
    # print(r.name)



