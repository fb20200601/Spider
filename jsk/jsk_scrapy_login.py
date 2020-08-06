import scrapy
import json
from jsk.sqldata import SqlData
from jsk.items import JskItem
from lxml import etree
import time
import random
import datetime


class JskSpiderSpider(scrapy.Spider):
    name = 'jsk_spider_demo'
    allowed_domains = ['jiansheku.com']
    # start_urls = ['http://jiansheku.com/']
    custom_settings = {
        'MYSQL_DB_NAME': 'antb_fb',
        'MYSQL_HOST': '192.168.1.5',
        'MYSQL_USER': 'cun',
        'MYSQL_PORT': '3306',
        'MYSQL_PASSWORD': '123456',

        # 'MYSQL_DB_NAME': 'antb',
        # 'MYSQL_HOST':'127.0.0.1',
        # 'MYSQL_USER':'root',
        # 'MYSQL_PORT' :'3306',
        # 'MYSQL_PASSWORD':'qazwsx123',
        "DOWNLOADER_MIDDLEWARES": {
            # 'jsk.middlewares.AgentDownloaderMiddleware': 543,
            # 'jsk.middlewares.SeleniumDownloaderMiddleware': 500,
            'jsk.middlewares.ProxyDownloaderMiddleware': 400,
        },
        # "DOWNLOAD_DELAY": random.random()+0.6
    }

    def start_requests(self):
        headers = {  # 登录抓包获取的头部
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Content-Type": "application/json",
            # "X-Requested-With": "XMLHttpRequest",
            # "Content-Length": "63",
            # "Connection": "keep-alive",
            # "dnt": "1",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "cors",
            # "Sec-Fetch-Site": "same-origin",
            # "Referer": "https://www.jiansheku.com/login.html",
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
        url = "https://www.jiansheku.com/api/jsk/enterprise/search"
        companys = SqlData.search_dblist()
        for company in companys:
            print("正在爬取的id是：" + str(company[2]) + ":" + str(company[1]))
            payload = {"pageIndex": "1", "pageSize": "10", "orderFlag": "0", "companyName": "{}".format(company[1])}
            # _data = json.dumps(payload)
            yield scrapy.FormRequest(url=url, formdata=payload, headers=headers, cookies=cookie, callback=self.parse)

    def parse(self, response):
        print(response.text)
        # item = JskItem()
        # company = response.meta.get("item")
        # context = json.loads(response.text)
        # contents = context["data"]['list']
        # if contents == []:
        #     print("此公司无匹配")
        #     item['b_find'] = '0'
        #     yield item
        # else:
        #     for content in contents:
        #         if content['bidCount'] == 0:
        #             continue
        #         else:
        #             corpname = '<div id="name_text">' + str(content['companyName']) + '</div>'
        #             hisname = '<div id="name_text">' + str(content['historyNames']) + '</div>'
        #             _corpname = etree.HTML(corpname)
        #             _hisname = etree.HTML(hisname)
        #             corpname_str = str(_corpname.xpath('string(//*[@id="name_text"])'))  # 去掉标签 纯文字
        #             hisname_str = str(_hisname.xpath('string(//*[@id="name_text"])'))  # 去掉标签 纯文字
        #             if company[1] == corpname_str:
        #                 item['jsk_urlid'] = content['id']
        #                 item['corp_id'] = company[0]
        #                 item['corpname'] = corpname_str
        #                 item['curname'] = corpname_str
        #                 item['hisname'] = hisname_str
        #                 item['yj_num'] = content['bidCount']
        #                 item['created_by'] = 'fb'
        #                 item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #                 item['b_find'] = '1'
        #                 print(item)
        #                 # yield item
        #             else:
        #                 print("公司匹配有误")
