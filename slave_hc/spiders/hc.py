# -*- coding: utf-8 -*-
import json
import re

from scrapy import Spider,Request
import pymongo
import redis
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TimeoutError
from hc_item.items import HcItemItem


class HcSpider(Spider):
    name = 'hc'
    allowed_domains = ['b2b.hc360.com','hc360.com']
    # start_urls = ['http://s.hc360.com/']
    # start_urls = []
    # client = pymongo.MongoClient('localhost')
    # db = client['new_hc']
    # pool = redis.ConnectionPool(host='47.107.137.63', port=6379, db=10,password='caonima')
    r = redis.Redis(host='47.107.137.63', port=6379, db=10,password='caonima',decode_responses=True)
    print(r)

    # redis_key = 'j_urls'
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(HcSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if "j_urls" in self.r.keys():
            while True:
                try:
                    datas = self.r.spop("j_urls")
                    string = re.sub("\'", '\"', datas)
                    # print(string)
                    data = json.loads(string)
            # string = str(self.r.get(i), encoding = "utf8")
            # string = re.sub("\'", '\"', string)
            # data = json.loads(string)
        # for i in self.r.lrange('yi:start_urls', 1, 10000):
        #     string = str(i, encoding="utf8")
                #     url = re.sub("\'", '\"', string)
                    item = HcItemItem()
                    item['tag'] =data['tag']
                    print(data['link'],'+++++++++++++++++++++++++++++++')
                    yield Request(data['link'], meta={'dont_redirect': True, 'item': item}, callback=self.parse,dont_filter=True)
                except ValueError:
                    print("xpath结果为空！")
                    pass
                except TimeoutError:
                    print("Proxy  not .......")

                except Exception as e:
                    if "j_urls" not in self.r.keys():
                        print("爬取结束,关闭爬虫！")
                        break
                    else:
                        print("请求发送失败", e.args)
                        # raise
                        continue
        else:
            print("No keys")

    def parse(self, response):
        # item = HcItemItem()
        item = response.meta['item']
        item['link'] = response.url
        area = response.xpath("//div[@class='proInfoAlert']/ul/li[3]/text()")
        new_area = response.xpath("//div[@class='view-con-l']/ul/li[2]/span/text()")
        if area:
            item['city'] = ''.join(''.join(area.extract()).strip('\r\n').strip('\t\r\n  ').split('\xa0'))
        elif new_area:
            item['city'] = new_area.extract()[-1]
        else:
            item['city'] = None
        fa = response.xpath("//div[@class='word1 part1']/div[@class='p name']/em/text()")
        item['contacts'] = fa.extract_first().strip('：').split('\xa0')[0] if fa else None
        name = response.xpath("//div[@class='word1 part1']/div[@class='p sate']/em/text()")
        item['name'] = name.extract_first().strip('：') if name else None
        tel2 = response.xpath("//div[@class='word1 part1']/div[@class='p tel2']/em/text()")
        item['tel2'] = tel2.extract_first().strip('：') if tel2 else None
        tel1 = response.xpath("//div[@class='word1 part1']/div[@class='p tel1']/em/text()")
        item['tel1'] = tel1.extract_first().strip('：').strip(' \xa0\xa0  ') if tel1 else None
        # print(item)
        yield item





