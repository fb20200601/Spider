# -*- coding: utf-8 -*-
# @Time    : 2020/7/23 11:30
# @Author  : Fang
# @FileName: zhihu.py
# @Software: PyCharm
import base64
import hashlib
import hmac
import json
import re
import threading
import time
from http import cookiejar

import requests
import execjs
from PIL import Image
from fake_useragent import UserAgent
from urllib.parse import urlencode


class Account(object):
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        # 账号密码预先留空
        self.login_data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'source': 'com.zhihu.web',
            'username': '',
            'password': '',
            'lang': 'en',
            'ref_source': 'other_https://www.zhihu.com/signin?next=%2F',
            'utm_source': ''
        }
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar(filename='./cookies.txt')

        self.ua = UserAgent()
        self.session.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
            # 随机UA
            'User-Agent': self.ua.random
        }

    def login(self, captcha_lang: str = 'en', load_cookies: bool = True):
        """
        模拟登陆
        :param captcha_lang: 验证码类型 'en' 或者 'cn'，默认为'en'
        :param load_cookies: 是否加载cookie文件，默认为True
        :return: bool，登陆结果
        """
        if load_cookies and self.load_cookies():
            print("读取 Cookie 文件")
            if self.check_login():
                print("登陆成功")
                return True
            else:
                print("Cookie 已失效，重新登陆中……")
        # 如果没有设置读取Cookie或者Cookie失效，则进入登陆流程
        self.check_account_info()
        # 将预留的空参数更新为登陆信息
        self.login_data.update({
            'username': self.username,
            'password': self.password,
            'lang': captcha_lang
        })
        # 登陆信息中用到的时间戳为13位
        timestamp = int(time.time() * 1000)
        self.login_data.update({
            'captcha': self.get_captcha(self.login_data['lang']),
            'timestamp': timestamp,
            'signature': self.get_signature(timestamp)
        })
        headers = self.session.headers.copy()
        headers.update({
            'content-type': 'application/x-www-form-urlencoded',
            'x-zse-83': '3_2.0',
            'x-xsrftoken': self.get_xsrf()
        })
        data = self.encrypt(self.login_data)
        login_api = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        res = self.session.post(login_api, data=data, headers=headers)
        if 'error' in res.text:
            print(json.loads(res.text)['error'])
        if self.check_login():
            print('登录成功')
            return True
        print('登录失败')
        return False

    def load_cookies(self):
        """
        读取Cookies文件
        :return: bool
        """
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except FileNotFoundError:
            return False

    def check_login(self):
        """
        检查登陆是否成功，访问登陆页面如果出现跳转则已经登陆
        如果登陆成功，保存当前Cookie到文件
        :return: bool
        """
        res = self.session.get('https://www.zhihu.com/signup', allow_redirects=False)
        if res.status_code == 302:
            self.session.cookies.save()
            return True
        return False

    def get_xsrf(self):
        """
        从登陆页面的set-Cookie参数中获取xsrf
        :return: str
        """
        self.session.get('https://www.zhihu.com/', allow_redirects=False)
        for c in self.session.cookies:
            if c.name == '_xsrf':
                return c.value
        raise AssertionError('获取 xsrf 失败')

    def get_captcha(self, lang: str):
        """
        请求验证码，必需运行，如果需要验证码则会接收到一个图片的base64编码
        需要人工输入验证码
        :param lang: 返回验证码的语言 'en'或'cn'
        :return: 用户提交的验证码验证输入
        """
        api='https://www.zhihu.com/api/v3/oauth/captcha?lang='+lang
        resp = self.session.get(api)
        show_captcha = re.search(r'true', resp.text)

        if show_captcha:
            put_resp = self.session.put(api)
            json_data = json.loads(put_resp.text)
            img_base64 = json_data['img_base64'].replace(r'\n', '')
            with open('./captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open('./captcha.jpg')
            if lang == 'cn':
                import matplotlib.pyplot as plt
                plt.imshow(img)
                print('点击所有倒立的汉字，在命令行中按回车提交')
                points = plt.ginput(7)
                capt = json.dumps({'img_size': [200, 44],
                                   'input_points': [[i[0] / 2, i[1] / 2] for i in points]})
            else:
                img_thread = threading.Thread(target=img.show, daemon=True)
                img_thread.start()
                capt = input('请输入图片里的验证码：')
            # 这里必须先把参数 POST 验证码接口
            self.session.post(api, data={'input_text': capt})
            return capt
        return ''

    def get_signature(self, timestamp: int or str):
        """
        通过HMAC算法计算返回签名
        :param timestamp: 时间戳
        :return: 签名
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + str(timestamp)), 'utf-8'))
        return ha.hexdigest()

    def check_account_info(self):
        """
        检查用户的账号密码输入情况，没有的话手动输入
        :return:
        """
        if not self.username:
            self.username = input('请输入手机号：')
        if self.username.isdigit() and '+86' not in self.username:
            self.username = '+86' + self.username

        if not self.password:
            self.password = input('请输入密码：')

    @staticmethod
    def encrypt(post_data: dict):
        """
        加密用户登陆信息
        :param post_data: 用户登陆信息
        :return: 加密后的信息，str
        """
        with open('./encrypt.js') as f:
            js = execjs.compile(f.read())
            return js.call('b', urlencode(post_data))


if __name__ == '__main__':
    account = Account('', '')
    account.login(captcha_lang='en', load_cookies=False)
    res = account.session.get('https://www.zhihu.com/api/v4/me')
    print(json.dumps(json.loads(res.text), indent=4, ensure_ascii=False))
