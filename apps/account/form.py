# -*- coding：utf-8 -*-

__author__ = 'madl'
__date__ = '2019/2/20 0020 下午 1:21'


from django import forms
from captcha.fields import CaptchaField
#对表单进行判断
class RegisterForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"}) #加入这条