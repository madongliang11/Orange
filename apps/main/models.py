import os
import time
import re

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models


# 导航栏
class Navigation(models.Model):
    nav_id = models.AutoField(verbose_name='ID', primary_key=True)
    nav_name = models.CharField(verbose_name=u'名称', max_length=64)
    is_delete = models.BooleanField()

    class Meta:
        db_table = 'navigation'
        verbose_name = u'导航栏'
        verbose_name_plural = verbose_name


# 商城头条
class Headline(models.Model):
    hid = models.AutoField(verbose_name='ID', primary_key=True)
    info = models.CharField(verbose_name=u'信息', max_length=255)
    status = models.BooleanField(verbose_name=u'状态')

    class Meta:
        db_table = 'headline'
        verbose_name = u'商城头条'
        verbose_name_plural = verbose_name


# 图片重命名
class ImageStorage(FileSystemStorage):
    IMG_PREFIX = 'IMG_'
    FILE_TIME = time.strftime('%Y%m%d%H%M%S')
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super().__init__(location, base_url)
        # 重写 _save方法

    # uploaad/img/img_afsfsfds.png
    # 修改文件的名称
    def _save(self, name, content):
        # 文件扩展名
        ext_name = name[name.rfind('.'):]
        # 文件目录
        image_path = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        image_name = self.IMG_PREFIX + self.FILE_TIME + ext_name
        image_file = os.path.join(image_path, image_name)
        # 调用父类方法
        return super()._save(image_file, content)


# 轮播图
class Banner(models.Model):
    banner_id = models.AutoField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name=u'标题', max_length=100)
    image = models.ImageField(verbose_name=u'轮播图', upload_to='banner/%Y%m%d', storage=ImageStorage(), max_length=100)
    detail_url = models.CharField(verbose_name=u'访问地址', max_length=200)
    order = models.IntegerField(verbose_name=u'顺序', default=1)
    create_time = models.DateTimeField(verbose_name=u'添加时间', auto_now_add=True)
    is_delete = models.BooleanField(verbose_name=u'状态')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'banner'
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def img_show(self):
        """
        后台显示图片
        :return:
        """
        return u'<img width=50px src="%s" />' % self.detail_url

    img_show.short_description = u'缩略图'
    # 允许显示HTML tag
    img_show.allow_tags = True


# 商品三级菜单
class Category(models.Model):
    cate_id = models.AutoField(verbose_name=u'分类ID', primary_key=True)
    # 当前类别所属父id
    parent_id = models.IntegerField(verbose_name=u'父ID')
    # 分类级别1/2/3   1代表一级菜单 2代表二级菜单 3代表三级菜单
    level = models.IntegerField(verbose_name=u'分类级别', null=False)
    # 商品名称
    name = models.CharField(verbose_name=u'商品名称', max_length=255, unique=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    # 0未删除  1删除
    is_delete = models.BooleanField(verbose_name=u'状态', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = u'分类菜单'
        verbose_name_plural = u'菜单管理'


# 商品表
class Shop(models.Model):
    shop_id = models.IntegerField(verbose_name=u'商品ID', primary_key=True)
    name = models.CharField(verbose_name=u'商品名称', max_length=100)
    original_price = models.DecimalField(verbose_name=u'原价', max_digits=7, decimal_places=2)
    promote_price = models.DecimalField(verbose_name=u'折扣价', max_digits=7, decimal_places=2)
    stock = models.IntegerField(verbose_name=u'库存')
    # 外键，与商品分类表Cate建立一对多关联
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True, verbose_name=u'商品分类')
    create_date = models.DateTimeField(verbose_name=u'创建时间', auto_now=True)
    # 是否热卖  0 非热卖  1热卖商品
    is_hot = models.BooleanField(verbose_name=u'热卖商品', default=False)
    # 销量
    sale = models.IntegerField(verbose_name=u'商品销量')
    # 排序 1表示升序  2表示降序
    sort = models.IntegerField(verbose_name=u'排序')
    # 商品状态 0有效  1删除
    is_delete = models.BooleanField(verbose_name=u'商品状态', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop'
        verbose_name = u'商品信息'
        verbose_name_plural = u'商品管理'


# 商品分类
class Search(models.Model):
    s_id = models.AutoField(verbose_name='ID', primary_key=True)
    # 外键
    shop = models.ForeignKey(verbose_name=u'商品id', to=Shop, on_delete=models.DO_NOTHING, db_column='cate_id')
    # 品牌
    brand = models.CharField(verbose_name=u'品牌', max_length=64)
    # 种类
    type = models.CharField(verbose_name=u'种类', max_length=64)
    # 选购热点
    buy_hot = models.CharField(verbose_name=u'选购热点', max_length=64)
    is_delete = models.BooleanField()

    class Meta:
        db_table = 'search'


# 商品详细参数名
class Property(models.Model):
    property_id = models.AutoField(verbose_name=u'商品参数名', primary_key=True)
    name = models.CharField(verbose_name=u'属性名称', max_length=64)
    # 外键，与商品表Shop建立一对多关联
    shop = models.ForeignKey(Shop, models.DO_NOTHING, db_column='shop_id', db_index=True, verbose_name=u"商品ID")
    is_delete = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'property'
        verbose_name = u'商品属性'
        verbose_name_plural = verbose_name


# 商品详细参数值
class PropertyValue(models.Model):
    pro_value_id = models.IntegerField(verbose_name='ID', primary_key=True)
    # shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='shop_id', verbose_name="商品ID")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_column='property_id', verbose_name=u"属性ID")
    value = models.CharField(verbose_name=u'属性值', max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'property_value'
        verbose_name = u'商品属性值'
        verbose_name_plural = verbose_name


# 商品图片
class Image(models.Model):
    img_id = models.AutoField(verbose_name='ID', primary_key=True)
    # 外键
    shop = models.ForeignKey(Shop, models.DO_NOTHING, db_column='shop_id', db_index=True, verbose_name=u'商品名称')
    type = models.CharField(verbose_name=u'图片类型', max_length=32, blank=True, null=True)
    img_url = models.CharField(verbose_name=u'图片名称', max_length=255)
    is_delete = models.BooleanField(verbose_name=u'状态', default=False)


    def __str__(self):
        return self.img_id

    class Meta:
        db_table = 'image'
        verbose_name = u'商品图片'
        verbose_name_plural = u'商品图片管理'

    def img_show(self):
        """
        后台显示图片
        :return:
        """
        return u'<img width=50px src="/static/img/small/%s.jpg" />' % self.img_url

    img_show.short_description = u'缩略图'
    # 允许显示HTML tag
    img_show.allow_tags = True


# 订单表
class Order(models.Model):
    ORDER_STATUS = (
        (1, '正常'),
        (0, '异常'),
        (-1, '删除'),
    )

    oid = models.AutoField(verbose_name=u'订单ID', primary_key=True)
    # 订单号唯一
    order_code = models.CharField(verbose_name=u'订单号', max_length=255)
    address = models.CharField(verbose_name=u'配送地址', max_length=255, )
    postcode = models.CharField(verbose_name=u'邮编', max_length=100)
    receiver = models.CharField(verbose_name=u'收货人', max_length=100)
    mobile = models.CharField(verbose_name=u'手机号', max_length=11, )
    user_message = models.CharField(verbose_name=u'附加信息', max_length=255)
    create_date = models.DateTimeField(verbose_name=u'创建日期', max_length=0)
    pay_date = models.DateTimeField(verbose_name=u'支付时间', max_length=0,
                                    blank=True, null=True)
    delivery_date = models.DateTimeField(verbose_name=u'交易日期', blank=True)
    confirm_date = models.DateTimeField(verbose_name=u'确认日期', blank=True)
    """ 1正常 0 异常, -1 删除 """
    status = models.IntegerField(verbose_name=u'订单状态', choices=ORDER_STATUS, default=1)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', verbose_name=u"用户ID",
                             related_name='user_order')

    class Meta:
        db_table = 'order'
        verbose_name = u'订单'
        verbose_name_plural = u'订单管理'


# 购物车表
class ShopCar(models.Model):
    car_id = models.AutoField(verbose_name='ID', primary_key=True)
    number = models.IntegerField(verbose_name=u'商品数量', default=0)
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, verbose_name=u'商品ID', related_name='shop_shopcar')
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, db_column='uid', verbose_name=u'用户ID',
                             related_name='user_shopcar')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, db_column='oid', null=True, verbose_name=u'商品ID',
                              related_name='order_shopcar')
    # 1正常 0删除 ， 禁止 2
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'shop_car'
        verbose_name = u'购物车'
        verbose_name_plural = verbose_name


# 用户表
# 拓展user
class User(AbstractUser):
    phone = models.CharField(verbose_name=u'手机号', max_length=11, default='110')
    desc = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='upload/img/%Y%m%d',
                             default=u"apps/static/img/default.png")
    _paypasswd = models.CharField(verbose_name=u'支付密码', max_length=128)
    id_num = models.CharField(verbose_name=u'身份证号', max_length=128)

    @property
    def paypasswd(self):
        return self._paypasswd

    @paypasswd.setter
    def paypasswd(self, paypasswd):
        # 支付密码加密
        self._paypasswd = make_password(paypasswd, 'pbkdf2_sha256')

    def verify_paypasswd(self, paypasswd):
        # 验证支付密码
        return check_password(paypasswd, self._paypasswd)

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def img_show(self):
        """
        后台显示图片
        :return:
        """
        return u'<img width=30px src="%s" />' % self.icon.url

    img_show.short_description = u'头像'
    # 允许显示HTML tag
    img_show.allow_tags = True


# 商品评论表
class Review(models.Model):
    review_id = models.AutoField(verbose_name='ID', primary_key=True)
    content = models.CharField(verbose_name=u'内容', max_length=4000, )
    create_date = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, db_column='shop_id', db_index=True, verbose_name=u"商品ID",
                             related_name='shop_review')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', db_index=True,
                             verbose_name=u'用户ID', related_name='user_review')
    is_delete = models.BooleanField()

    class Meta:
        db_table = 'review'
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name


# 商品收藏表
class Collect(models.Model):
    cid = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(User, models.CASCADE, db_column='uid', db_index=True, verbose_name=u"用户ID",
                             related_name='user_collect')
    shop = models.ForeignKey(Shop, models.CASCADE, db_column='shop_id', db_index=True, verbose_name=u"商品ID",
                             related_name='shop_collect')
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    is_delete = models.BooleanField()

    class Meta:
        db_table = 'collect'
        verbose_name = u'商品收藏'
        verbose_name_plural = verbose_name


# 用户地址表
class Address(models.Model):
    aid = models.AutoField(primary_key=True, verbose_name='地址ID')
    reciver = models.CharField(max_length=64,verbose_name='收件人')
    phone = models.CharField(max_length=20, verbose_name='收件人号码')
    province = models.CharField(max_length=64, verbose_name='省')
    city = models.CharField(max_length=64, verbose_name='市')
    area = models.CharField(max_length=64,verbose_name='区')
    detail_loc = models.CharField(max_length=255, null=False, verbose_name='详细地址')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='uid', db_index=True,
                             verbose_name="用户ID")
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 0正常地址  1默认地址
    status = models.IntegerField(default=0)
    is_detele = models.BooleanField()

    class Meta:
        db_table = 'address'
        verbose_name = u'用户地址'
        verbose_name_plural = verbose_name

# 地区表
class Area(models.Model):
    aid = models.AutoField(primary_key=True, verbose_name='地址ID')
    # 当前类别所属父id
    parent_id = models.IntegerField(verbose_name=u'父ID')
    short_name = models.CharField(verbose_name='地区简称',max_length=64)
    name = models.CharField(verbose_name='地区名', max_length=64)
    merger_name = models.CharField(verbose_name='全称', max_length=64)
    # 分类级别1/2/3   1代表一级菜单 2代表二级菜单 3代表三级菜单
    level = models.CharField(verbose_name=u'分类级别',max_length=64)
    pinyin = models.CharField(verbose_name='地区拼音',max_length=64)
    code = models.CharField(verbose_name='地区编号',max_length=64)
    zip_code = models.CharField(max_length=64)
    first = models.CharField(verbose_name='首字母',max_length=64)
    lng = models.CharField(verbose_name='经度',max_length=64)
    lat = models.CharField(verbose_name='维度',max_length=64)
    status = models.IntegerField(verbose_name=u'状态', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Area'
        verbose_name = u'地区信息'
        verbose_name_plural = u'地区信息'

