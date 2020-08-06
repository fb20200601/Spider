# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 8:43
# @Author  : Fang
# @FileName: selenium_login.py
# @Software: PyCharm
# @version: python 3.7
# -*- coding: utf-8 -*-
""" 
@author: fang 
@version: Python 3.7.0 
@software: PyCharm 
@file: tes.py 
@time: 2020/7/3 11:53 
"""
import time
from selenium import webdriver
import random


class Login(object):
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
        # 创建浏览器对象
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def sele(self):
        url = 'https://www.jiansheku.com/'
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(1.2)
        self.driver.find_element_by_class_name("login").click()
        time.sleep(3)
        self.driver.find_element_by_class_name('mmSign').click()
        time.sleep(2 + random.random())
        phone = self.driver.find_element_by_id('phone')
        phone.send_keys("18365230886")
        time.sleep(1 + random.random())
        password = self.driver.find_element_by_id('password')
        password.send_keys('jsk_17969')
        time.sleep(0.5 + random.random())
        # self.driver.find_element_by_class_name('button').click()
        self.driver.find_element_by_xpath(".//*[@class='button immediateLogin']").click()
        time.sleep(5.5)
        self.driver.get("https://www.jiansheku.com/qiye.html?key=%E5%AE%89%E5%BE%BD%E6%B0%B4%E5%AE%89%E5%BB%BA%E8%AE%BE%E9%9B%86%E5%9B%A2%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8")
        # for i in range(90):
        #     time.sleep(3 + random.random())
        #     self.driver.get("https://www.jiansheku.com/qy_21333/zb_{}.html".format(i))


if __name__ == '__main__':
    l = Login()
    l.sele()
