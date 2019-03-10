# 全局配置
import xadmin
from xadmin import views
from xadmin.plugins import auth

from apps.main.models import Navigation, Headline, Banner, Shop, User, Image


class BaseStyleSettings:
    # 开启修改主题
    enable_themes = True
    # 使用bootbootstarp的主题
    use_bootswatch = True


# 注册自定义全局配置
xadmin.site.register(views.BaseAdminView, BaseStyleSettings)


# 修改页眉页脚
class GlobalSettings:
    site_title = r'橘子商城'
    site_footer = r'橘子，爱你所爱'


xadmin.site.register(views.CommAdminView, GlobalSettings)


# 后台导航栏
class NavigationXadmin:
    # pass
    # 默认情况下显示object对象
    list_display = ['nav_id', 'nav_name']


xadmin.site.register(Navigation, NavigationXadmin)


# 后台轮播图
class BannerXadmin:
    list_display = ['banner_id', 'title', 'img_show', 'detail_url', 'order', 'create_time', 'is_delete']


xadmin.site.register(Banner, BannerXadmin)


# 后台新闻头条
class HeadlineXadmin:
    list_display = ['hid', 'info', 'status']


xadmin.site.register(Headline, HeadlineXadmin)


# 后台商品管理
class ShopXadmin:
    list_display = ['shop_id',
                    'name',
                    'original_price',
                    'promote_price',
                    'stock',
                    'cate',
                    'sale',
                    'sort',
                    'is_hot',
                    'create_date',
                    'is_delete'
                    ]
    list_per_page = 10
    search_fields = ['name', 'shop_id']


xadmin.site.register(Shop, ShopXadmin)


class ShopImageXadmin(ShopXadmin):
    list_display = ['img_id', 'img_show', 'shop', 'type', 'img_url', 'is_delete']


xadmin.site.register(Image, ShopImageXadmin)


class UserXadmin(auth.UserAdmin):
    list_display = ['id', 'username', 'img_show', 'email', 'phone', 'is_active', 'is_superuser']


xadmin.site.unregister(User)
xadmin.site.register(User, UserXadmin)
