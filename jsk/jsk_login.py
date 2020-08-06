# -*- coding: utf-8 -*-
# @Time    : 2020/8/4 14:10
# @Author  : Fang
# @FileName: jsk_login.py
# @Software: PyCharm
# @version: python 3.7

import requests
import json

session = requests.Session()
headers = {  # 登录抓包获取的头部
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "63",
    "Connection": "keep-alive",
    "dnt": "1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://www.jiansheku.com/login.html",
}
cookie = {
    "regionId": "340000",
    "UM_distinctid": "173b6fe9c46d36-05c4c744430bdb-87f1e3e-1fa400-173b6fe9c47155",
    "CNZZDATA1275173796": "409209790-1596502626-https%253A%252F%252Fwww.baidu.com%252F%7C1596502626",
    "Hm_lvt_03b8714a30a2e110b8a13db120eb6774": "1596510847",
    "isClose": "yes",
    "token": "6d39c18742d5441db3e0717bfc624e58",
    "Hm_lpvt_03b8714a30a2e110b8a13db120eb6774": "1596519776",
}


def login():
    url = "https://www.jiansheku.com/api/jsk/user/login"
    data = '{"userName":"18365230886","password":"jsk_17969","loginType":1}'
    try:
        content = session.post(
            url=url,
            headers=headers,
            data=data,
            cookies=cookie
        )
    except Exception as e:
        print(e)


def search():
    _url = "https://www.jiansheku.com/api/jsk/enterprise/search"
    _data = json.dumps({"pageIndex": 1, "pageSize": 10, "orderFlag": 0, "companyName": "安徽水安建设集团股份有限公司"})
    _cookie = {
        "isClose": "yes",
        "Hm_lvt_03b8714a30a2e110b8a13db120eb6774": "1596607452, 1596618886, 1596673383, 1596674693",
        "regionId": "100000",
        "token": "6d39c18742d5441db3e0717bfc624e58",
        "Hm_lpvt_03b8714a30a2e110b8a13db120eb6774": "1596675605"
    }
    _headers = {  # 登录抓包获取的头部
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "102",
        "Connection": "keep-alive",
        "dnt": "1",
        "token": "6d39c18742d5441db3e0717bfc624e58",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Referer": "https://www.jiansheku.com/qiye.html?key=%E5%AE%89%E5%BE%BD%E6%B0%B4%E5%AE%89%E5%BB%BA%E8%AE%BE%E9%9B%86%E5%9B%A2%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8",
        "Origin": "https://www.jiansheku.com"
    }
    item_list = session.post(_url, headers=_headers, cookies=_cookie, data=_data)
    context = json.loads(item_list.text)
    contents = context["data"]['list']
    for content in contents:
        print(content['id'])


if __name__ == '__main__':
    login()
    search()
