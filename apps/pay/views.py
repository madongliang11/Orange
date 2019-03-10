from alipay import AliPay
from django.shortcuts import render, redirect

# Create your views here.
from OrangeMall.settings import APP_ID, APP_PRIVATE_KEY_STR, APP_PUBLIC_KEY_STR, PAY_URL_DEV
from apps.main.models import Order


def our_pay(request):
    if request.method == 'GET':
        oid = request.GET.get('oid')
        amount= request.GET.get('total')
        aid = request.GET.get('aid')
        trad_no = Order.objects.filter(oid=oid).first().order_code
        alipay = AliPay(
            # 实例化Alipay对象
            appid=APP_ID,
            app_notify_url='http://127.0.0.1:8000/',
            app_private_key_string=APP_PRIVATE_KEY_STR,
            alipay_public_key_string=APP_PUBLIC_KEY_STR,
            sign_type='RSA2',
            debug=True,
        )

        # 生成支付的参数
        '''
        subject 支付的标题
        out_trade_no 生成的订单号
        total_amount 支付的总金额
        return_url  支付完成之后前端跳转的界面 get请求
        notify_url 支付完成后台回调接口  post请求
        '''

        order_string = alipay.api_alipay_trade_page_pay(
            # 订单号
            out_trade_no=trad_no,
            # 商品总价
            total_amount=str(amount),  # 将Decimal类型转换为字符串交给支付宝
            # 订单标题
            subject="橘子商城-{}".format(int(trad_no)),
            # 支付成功之后 前端跳转的界面
            return_url='http://127.0.0.1:8000/order/success/?order_code={0}&aid={1}&total={2}'.format(trad_no,aid,amount),
            # 支付成功后台跳转接口
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        return redirect(PAY_URL_DEV + order_string)



    ############################支付账号############################
    #买家账号uijaot7585@sandbox.com
    #登录密码111111
    #支付密码111111
    ################################################################
