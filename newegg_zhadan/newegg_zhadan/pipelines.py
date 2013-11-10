# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#coding=utf-8
import pymongo
from scrapy import log
import time
MONGODB_SAFE = False
MONGODB_ITEM_ID_FIELD = "_id"
class NeweggZhadanPipeline(object):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection, mongodb_uniq_key,
                 mongodb_item_id_field, mongodb_safe):
        connection = pymongo.Connection(mongodb_server, mongodb_port)
        self.mongodb_db = mongodb_db
        self.db = connection[mongodb_db]
        self.mongodb_collection = mongodb_collection
        self.collection = self.db[mongodb_collection]
        self.uniq_key = mongodb_uniq_key
        self.itemid = mongodb_item_id_field
        self.safe = mongodb_safe
        self.result_dict = {}

    def process_item(self, item, spider):
        if item['id'] in self.result_dict:
            if item['stat'] != self.result_dict[item['id']]['stat']:
                log.msg('stat error,id :%s cur:%d pro:%d'%(item['id'],item['stat'],self.result_dict[item['id']]['stat']),level=log.WARNING)
                if item['stat'] > self.result_dict[item['id']]['stat']:
                    self.result_dict[item['id']] = item
        else:
            self.result_dict[item['id']] = item
        return item

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('MONGODB_SERVER', 'localhost'), settings.get('MONGODB_PORT', 27037),
            settings.get('MONGODB_DB', 'scrapy'), settings.get('MONGODB_COLLECTION', None),
            settings.get('MONGODB_UNIQ_KEY', None), settings.get('MONGODB_ITEM_ID_FIELD', MONGODB_ITEM_ID_FIELD),
            settings.get('MONGODB_SAFE', MONGODB_SAFE))

    def close_spider(self,spider):
        for (id,item) in self.result_dict.items():
            self.collection.update({self.uniq_key: item[self.uniq_key] }, {'$set':dict(item) },upsert=True, safe=self.safe)
