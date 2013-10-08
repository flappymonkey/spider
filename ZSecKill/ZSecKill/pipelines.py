#coding=utf-8
import pymongo
from scrapy import log
import time
MONGODB_SAFE = False
MONGODB_ITEM_ID_FIELD = "_id"

class ZseckillPipeline(object):
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
        #print item['title'],item
        if item['id'] in self.result_dict:
            log.msg('%s already process %d'%(item['id'],item['stat']))
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
        return cls(settings.get('MONGODB_SERVER', 'localhost'), settings.get('MONGODB_PORT', 27017),
            settings.get('MONGODB_DB', 'scrapy'), settings.get('MONGODB_COLLECTION', None),
            settings.get('MONGODB_UNIQ_KEY', None), settings.get('MONGODB_ITEM_ID_FIELD', MONGODB_ITEM_ID_FIELD),
            settings.get('MONGODB_SAFE', MONGODB_SAFE))

    def close_spider(self,spider):
        get_time = int(time.time()) - 86400 * 2
        db_result = self.collection.find({'source':'Z秒杀','actual_time_begin':{'$gte':get_time}},{'id':1,'stat':1})
        db_result_dict = {}
        for item in db_result:
            db_result_dict[item['id']] = item
        all_count_dict = {}
        noin_count_dict = {}
        all_count_dict[1] = 0
        all_count_dict[2] = 0
        all_count_dict[3] = 0
        noin_count_dict[1] = 0
        noin_count_dict[2] = 0
        noin_count_dict[3] = 0
        for (id,item) in self.result_dict.items():
            all_count_dict[item['stat']] += 1
            if id not in db_result_dict:
                if item['stat'] == 2:
                    item['actual_time_begin'] = int(time.time())
                    item['display_time_begin'] = item['actual_time_begin']
                noin_count_dict[item['stat']] += 1
            if id not in db_result_dict or db_result_dict[id] != 4:
                self.collection.update({self.uniq_key: item[self.uniq_key] }, {'$set':dict(item) },upsert=True, safe=self.safe)
        log.msg('数据库获取商品数:%d 不在数据库中商品数:%d-%d-%d 即将开始:%d 进行中:%d 已经结束:%d'%(len(db_result_dict),noin_count_dict[1],noin_count_dict[2],noin_count_dict[3],all_count_dict[1],all_count_dict[2],all_count_dict[3]),level=log.INFO)
