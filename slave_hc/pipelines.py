# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from hc_item.items import HcItemItem
import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('./js_items.json', 'a')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.i = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        # if isinstance(item,HcItemItem):
        collection = 'hc_item_净水'
        # if self.db[collection].update({'name': item['name']}, {'$set': dict(item)}, True):
        if item['name']:
            if self.db[collection].update({'name':item['name']},{'$set': dict(item)},True):
                print('Sueecss saved to Mongodb',item['name'])
                self.i +=1
                print(self.i)
            else:
                print('Not Mongodb ')
        # elif isinstance(item,HcItem):
        #     collection = 'hc_item2'
        #     if self.db[collection].insert(dict(item)):
        #         print('Sueecss saved to Mongodb',item['name'])
        return item

class HcItemPipeline(object):
    def process_item(self, item, spider):
        return item
