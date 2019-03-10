# -*- coding: utf-8 -*-  


'''
web浏览器配置文件
走有头，无头浏览器
'''

from selenium import webdriver

def create_bs_driver(type="firefox", headless=False):
	'''
	:param type:
	:param headless:  是否为无头浏览器，True---无头，  False---有头
	:return:
	'''
	if type == "firefox":   #火狐浏览器
		firefox_opt = webdriver.FirefoxOptions()
		firefox_opt.add_argument("--headless") if headless else None
		driver = webdriver.Firefox(firefox_options=firefox_opt)
	elif type == "chrome":  #谷歌浏览器
		chrome_opt = webdriver.ChromeOptions()
		chrome_opt.add_argument("--headless") if headless else None
		driver = webdriver.Chrome(chrome_options=chrome_opt)
	else:
		return None
	return driver





