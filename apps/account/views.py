import re

from django.contrib.auth.decorators import  login_required
from django.contrib.auth import logout, login ,authenticate
from django.db.models import Q
from django.shortcuts import render, redirect

from apps.account.form import RegisterForm
from apps.main.models import User
from django.template import loader
from apps.account.tasks import send_active_mail

#登录
def login_view(request):
    if request.method == 'GET':
        login_form = RegisterForm()
        return render(request,'login.html',{'login_form':login_form})
    elif request.method == 'POST':
        try:
            login_form = RegisterForm(request.POST)
            if login_form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                # 判断密码和账号输入是否为空
                if username and password:
                    # 认证一组给定的用户和密码,如果密码能够匹配给定的用户名，
                    # 它将返回一个User对象，如果密码无效，authenticate()返回None
                    user = authenticate(username=username,password=password)
                    # 验证码验证

                    if user is not None:
                        #用户名密码正确
                        if user.is_active:
                            #用户已激活
                            #记录用户的登录状态
                            login(request,user)
                            #跳转到首页
                            return redirect('/')
                        else:
                            #用户未激活
                            return render(request,'login.html',{'msg':'账户未激活'})
                    else:
                        #用户名密码错误
                        return render(request,'login.html',{'msg':'用户名或密码错误'})
                else:
                    return render(request,'login.html',{'msg':'账号或密码不能为空'})
            else:
                return render(request,'login.html',{'login_form':login_form})
        except Exception as e:
            return render(request,'login.html',{'msg':'登录失败'})
    else:
        return render(request,'login.html',{'msg':'无效请求方式'})


#注册
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            pwdRepeat = request.POST.get('pwdRepeat')

            # 判断输入用户名、密码.....输入是否为空
            if username and password and phone and email and pwdRepeat:
                user = User.objects.filter(Q(username=username) | Q(phone=phone) | Q(email=email))
                #判断输入的信息是否存在
                if user.exists():
                    return render(request,'register.html',{'msg':'用户名、手机号或邮箱已占用！'})
                else:
                    #判断电话号码
                    if re.match(r'^1[35678]\d{9}$',phone):
                        #判断邮箱
                        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
                            #判断两次密码是否一致 和密码长度
                            if password == pwdRepeat and len(password) > 5:
                                # 保存用户操作
                                user = User.objects.create_user(username=username, password=password, phone=phone,
                                                                email=email,is_active=0)
                                if user:
                                    # 如果注册成功，直接记住用户登录状态，跳转登录界面
                                    # login(request, user)
                                    # # 反向解析
                                    # url = reverse('account:login')
                                    # return redirect(url)
                                    active_url = f"http://127.0.0.1:8000/account/active/?uid={user.id}"
                                    content = loader.render_to_string('mail.html',
                                                                      request=request,
                                                                      context={'username':username,
                                                                               'active_url':active_url})
                                    send_active_mail.delay(subject='甜橙项目激活邮件', content=content, to=['15565608583@163.com'])
                                    return render(request, 'msg.html')
                                else:
                                    return render(request, 'register.html', {'msg': '注册失败'})
                            else:
                                return render(request, 'register.html', {'msg': '两次密码不一样或密码太短'})
                        else:
                            return render(request, 'register.html', {'msg': '输入正确邮箱'})
                    else:
                        return render(request, 'register.html', {'msg': '输入正确的手机号'})
            else:
                return render(request, 'register.html', {'msg': '输入信息不能为空'})
        except Exception as e:
           return render(request,'404.html')
    else:
        return render(request,'404.html')



def logout_view(request):
    logout(request)
    return redirect('/')

#验证用户是否登录
@login_required(login_url='/account/login/')
def update(request):
    user = request.user
    return redirect('/')

def detall(request):
    pass


def active_account(request):
    uid = request.GET.get('uid')
    User.objects.filter(id=uid).update(is_active=1)
    return redirect('/account/login')
