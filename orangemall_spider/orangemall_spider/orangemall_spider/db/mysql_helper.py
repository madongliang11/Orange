# -*- coding: utf-8 -*-  

'''
采用sqlalchemy第三方库，来实现orm操作
依赖库：
  pip  install  sqlalchemy
  pip  install  pymysql
'''

import threading


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import MYSQL_SETTINGS

mysql_conn_str = f"mysql+pymysql://{MYSQL_SETTINGS['user']}:{MYSQL_SETTINGS['passwd']}@{MYSQL_SETTINGS['host']}:{MYSQL_SETTINGS['port']}/{MYSQL_SETTINGS['db']}?charset=utf8"

engine = create_engine(mysql_conn_str)

# models.Model
Base = declarative_base()  # 生成orm基类，自定义业务orm类继承此类，也就具有orm特性

'''
定义一个sqlalchemy操作类，封装orm的增删改查操作
'''


class MySQLORMHelper(object):

    def __create_db_table(self):
        '''
        基于engine同步数据库模型
        :return:
        '''
        Base.metadata.create_all(engine)

    def create_session(self):
        '''
        创建session，用于增删改查操作, 返回session对象
        :return:
        '''
        self.__create_db_table()
        Session = sessionmaker(bind=engine)
        return Session()

    def add_records(self, session, objs):

        '''
        添加orm对象数据到数据库
        :param session:
        :param objs: 对象列表  or   对象
        :return:
        '''
        if isinstance(objs, list):  # 对象列表，[obj1, obj2, obj3, obj4]
            session.add_all(objs)
        else:  # obj
            session.add(objs)
        try:
            session.commit()
        except Exception as e:
            session.rollback()

    def update_record(self, session, Cls, cd_field, cd_value, up_dict):
        '''
        更新数据库操作
        eg: update  student， class  set  age=20    where student.cid=clsss.id and id=110
        :param session:
        :param Cls:  需要更新的orm类   （eg: Student）
        :param cd_field: 更新条件字段   (eg: Student.id)
        :param cd_value:  更新条件值    (110)
        :param up_dict:  更新的字典     ({'age':20})
        :return:
        '''
        flag = session.query(Cls).filter(cd_field == cd_value).update(up_dict)
        if flag:
            session.commit()
            return True
        else:
            return False

    def query_records(self, session, Cls):
        '''
        查询orm类中所有的记录数
        :param session:
        :param Cls:
        :return:
        '''
        return session.query(Cls).all()

    def query_conditions(self, session, Cls, cd_field, cd_value):
        '''
        查询满足条件的db数据
        :param Cls:
        :param cd_field:
        :param cd_value:
        :return:
        '''
        result =  session.query(Cls).filter(cd_field == cd_value)
        # print(result)
        return result

    def delete_records(self, session, Cls, field, value):
        '''
        删除数据库记录
        eg:delete  from   student  where id=120
        :param session:
        :param Cls:    Student
        :param field:   Student.id
        :param value:   120
        :return:
        '''
        flag = session.query(Cls).filter(field == value).delete()
        if flag:
            session.commit()
            return True
        else:
            return False
