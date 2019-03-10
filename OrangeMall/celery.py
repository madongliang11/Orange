
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# 设置项目的配置文件    ‘项目名称.settings’
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrangeMall.settings')
# 实例化celery 一个工程中可以实例化多个  但是django中是没有必要实例化多个celery对象
# Celery('dj_celery')  参数是项目的名称
# app = Celery('dj_celery')
app = Celery('Orange',broker='redis://127.0.0.1:6379/2')
# 加载celery配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')
# 自动注册app中的tasks文件
app.autodiscover_tasks()

# 开启debug模式
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))