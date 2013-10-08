#coding=utf-8

import json
import codecs
import traceback
import pymongo
import datetime
from urllib import unquote
from scrapy import log

MONGODB_SAFE = False
MONGODB_ITEM_ID_FIELD = "_id"

class SmzdmPipeline(object):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection, mongodb_uniq_key,
                 mongodb_item_id_field, mongodb_safe,output_file):
        self.file = codecs.open(output_file,'w',encoding='UTF-8')
        connection = pymongo.Connection(mongodb_server, mongodb_port)
        self.mongodb_db = mongodb_db
        self.db = connection[mongodb_db]
        self.mongodb_collection = mongodb_collection
        self.collection = self.db[mongodb_collection]
        self.uniq_key = mongodb_uniq_key
        self.itemid = mongodb_item_id_field
        self.safe = mongodb_safe

        if isinstance(self.uniq_key, basestring) and self.uniq_key == "":
            self.uniq_key = None

        if self.uniq_key:
            self.collection.ensure_index(self.uniq_key, unique=True)

        self.out_dict = {}
        self.temp_dict = {}
        self.temp_link_dict = {}
        self.url_filter_dict = {}
        self.crawl_num_dict = {}
        self.new_item_dict = {}
        self.same_id_dict = {}
        self.total_crawl_num = 0
        self.in_db_num = 0
        self.may_same_num = 0
        self.new_num = 0
        self.delete_num = 0
    def _parse_list_merge(self,cur_list):
        cur_str = ''
        if cur_list:
            for item in cur_list:
                cur_str = cur_str + item + ' '
            return cur_str[:-1]
        else:
            return ''
    def _parse_list_list_merge(self,cur_list):
        cur_str = ''
        if cur_list:
            for temp_list in cur_list:
                cur_str = cur_str + temp_list[0] + ':' + temp_list[1] + '|'
            return cur_str[:-1]
        else:
            return ''
    def _output_item(self,item):
        log.msg('ID: %s'%item['id'],level = log.WARNING)
        log.msg('抓取来源: %s'%item['crawl_source'],level = log.WARNING)
        log.msg('原始url: %s'%item['source_url'],level = log.WARNING)
        log.msg('商城: %s'%self._parse_list_merge(item['source']),level = log.WARNING)
        log.msg('标题: %s'%self._parse_list_merge(item['title']),level = log.WARNING)
        log.msg('描述: %s'%self._parse_list_merge(item['desc']),level = log.WARNING)
        log.msg('链接: %s'%self._parse_list_list_merge(item['desc_link_list']),level = log.WARNING)
        log.msg('直达链接: %s'%self._parse_list_list_merge(item['go_link']),level = log.WARNING)
        log.msg('图片: %s'%self._parse_list_merge(item['img']),level = log.WARNING)
        log.msg('分类: %s'%self._parse_list_merge(item['cat']),level = log.WARNING)
        log.msg('更新时间: %s'%item['pub_time'],level = log.WARNING)
    def process_item(self, item, spider):
        item['desc_link_list'] = []
        item['go_link'] = []
        if item['flag'] == 0:
            if not item['id'] in self.out_dict:
                if item['id'] in self.temp_dict:
                    for (desc,link) in self.temp_dict[item['id']].items():
                        #item['desc_link_list'][desc] = link
                        temp_list = []
                        temp_list.append(desc)
                        temp_list.append(link)
                        item['desc_link_list'].append(temp_list)
                if item['id'] in self.temp_link_dict:
                    for (desc,link) in self.temp_link_dict[item['id']].items():
                        temp_list = []
                        temp_list.append(desc)
                        temp_list.append(link)
                        item['go_link'].append(temp_list)
                        #item['go_link'][desc] = link
                self.out_dict[item['id']] = item
        elif item['flag'] == 1:
            if item['id'] in self.out_dict:
                temp_list = []
                temp_list.append(item['link_desc'])
                temp_list.append(item['link'])
                (self.out_dict[item['id']])['desc_link_list'].append(temp_list)
                #(self.out_dict[item['id']])['desc_link_list'][item['link_desc']] = item['link']
            else:
                if item['id'] in self.temp_dict:
                    self.temp_dict[item['id']][item['link_desc']] = item['link']
                else:
                    self.temp_dict[item['id']] = {}
        else:
            if item['id'] in self.out_dict:
                temp_list = []
                temp_list.append(item['link_desc'])
                temp_list.append(item['link'])
                (self.out_dict[item['id']])['go_link'].append(temp_list)
                #(self.out_dict[item['id']])['go_link'][item['link_desc']] = item['link']
            else:
                if item['id'] in self.temp_link_dict:
                    self.temp_link_dict[item['id']][item['link_desc']] = item['link']
                else:
                    self.temp_link_dict[item['id']] = {}
        return item

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('MONGODB_SERVER', 'localhost'), settings.get('MONGODB_PORT', 27017),
            settings.get('MONGODB_DB', 'scrapy'), settings.get('MONGODB_COLLECTION', None),
            settings.get('MONGODB_UNIQ_KEY', None), settings.get('MONGODB_ITEM_ID_FIELD', MONGODB_ITEM_ID_FIELD),
            settings.get('MONGODB_SAFE', MONGODB_SAFE),settings.get('OUTPUT_FILE', 'output_result.json'))

    def close_spider(self,spider):
        #从数据库中根据条件获取数据
        db_result = []
        sorted_list = sorted(self.out_dict.items(), key=lambda d:d[1]['pub_time'],reverse=True)
        if spider.scrapy_mode == 2:
            day_diff = spider.max_time_diff / 86400
            sec_diff = spider.max_time_diff % 86400
            cur_time_diff = datetime.timedelta(days = day_diff,seconds = sec_diff)
            cur_date = (spider.cur_date - cur_time_diff).strftime('%Y-%m-%d %H:%M:%S')
            db_result = self.collection.find({"pub_time":{"$gte":cur_date}})
            log.msg('get data from db pub_time gte %s'%cur_date,level=log.WARNING)
            #print 'get data gte',cur_date
        elif spider.scrapy_mode == 1:
            if sorted_list:
                (key,item) = sorted_list[-1]
                db_result = self.collection.find({"pub_time":{"$gte":item['pub_time']}})
                log.msg('get itmes num[%d] from db where pub_time gte %s'%(len(db_result),cur_date),level=log.DEBUG)
        else:
            db_result = self.collection.find()

        get_result_dict = {}
        for cur_item in db_result:
            get_result_dict[cur_item['id']] = cur_item
            for temp_list in cur_item['go_link']:
                url = temp_list[1]
                temp_dict = {}
                temp_dict['crawl_source'] = cur_item['crawl_source']
                temp_dict['id'] = cur_item['id']
                self.url_filter_dict[url] = temp_dict
        #print 'get result num from db',len(get_result_dict)
        log.msg('get itmes num[%d] from db where pub_time gte %s'%(len(get_result_dict),cur_date),level=log.DEBUG)
        log.msg('get result num[%d] from db'%len(get_result_dict),level=log.WARNING)
        #for (key,item) in sorted(self.out_dict.items(), key=lambda d:d[1]['pub_time'],reverse=True):
        for (key,item) in sorted_list:
            try:
                if item['crawl_source'] not in self.crawl_num_dict:
                    self.crawl_num_dict[item['crawl_source']] = 1
                else:
                    self.crawl_num_dict[item['crawl_source']] += 1
                self.total_crawl_num += 1
                if key in get_result_dict:
                    #print 'find key in db',key,get_result_dict[key]['stat']
                    self.in_db_num += 1
                    log.msg('find id[%s] in db,db item stat[%d]'%(key,get_result_dict[key]['stat']),level=log.DEBUG)
                    if get_result_dict[key]['stat'] != 2:
                        del get_result_dict[key]
                        log.msg('id[%s] in db,filter'%key,level=log.DEBUG)
                        #print key,'in db'
                        continue
                    else:
                        #print 'change stat for item:',key
                        log.msg('id[%s] in db need change stat to %d'%(key,0),level=log.WARNING)
                        item['stat'] = 0
                        del get_result_dict[key]
                else:
                    self.new_num += 1
                    if item['crawl_source'] not in self.new_item_dict:
                        self.new_item_dict[item['crawl_source']] = 1
                    else:
                        self.new_item_dict[item['crawl_source']] += 1
                    log.msg('id[%s] not in db[%s][%s]'%(key,item['crawl_source'],item['pub_time']),level=log.WARNING)
                    #self._output_item(item)
                    for temp_list in item['go_link']:
                        #ct = temp_list[0]
                        url = temp_list[1]
                        if url in self.url_filter_dict:
                            #print url,'in dict',item['id'],self.url_filter_dict[url]['id'],item['crawl_source'],self.url_filter_dict[url]['crawl_source']
                            log.msg('link url[%s] seen before,maybe same item,curid[%s] from[%s], same_id[%s] from[%s]'%(url,item['id'],item['crawl_source'],self.url_filter_dict[url]['id'],self.url_filter_dict[url]['crawl_source']),level=log.WARNING)
                            if cmp(item['crawl_source'],self.url_filter_dict[url]['crawl_source']) != 0:
                                #print 'different source',item['crawl_source'],self.url_filter_dict[url]['crawl_source']
                                log.msg('from different source may filter curid[%s] from[%s], same_id[%s] from[%s]'%(item['id'],self.url_filter_dict[url]['id'],item['crawl_source'],self.url_filter_dict[url]['crawl_source']),level=log.WARNING)
                                #item['same_id'] = self.url_filter_dict[url]['id']
                                self.same_id_dict[item['id']] = self.url_filter_dict[url]['id']
                                self.same_id_dict[self.url_filter_dict[url]['id']] = item['id']
                                #self.url_filter_dict[url]['id'] = item['id']
                                self.may_same_num += 1
                        else:
                            temp_dict = {}
                            temp_dict['crawl_source'] = item['crawl_source']
                            temp_dict['id'] = item['id']
                            self.url_filter_dict[url] = temp_dict
                line = json.dumps(dict(item)) + '\n'
                self.file.write(line)
                #write to db
                if self.uniq_key is None:
                    result = self.collection.insert(dict(item), safe=self.safe)
                else:
                    result = self.collection.update({self.uniq_key: item[self.uniq_key] }, { '$set': dict(item) },upsert=True, safe=self.safe)
                    #result = self.collection.insert(dict(item), safe=self.safe)
            except Exception, e:
                log.msg('error info[%r,%r]'%(e,traceback.format_exc()),level=log.WARNING)
                self._output_item(item)
                #print e
                #print traceback.format_exc()
                #print item
        for (key,item) in get_result_dict.items():
            #页面上不设置展现时间的，不进行无效性设置
            log.msg('need_filter:%d,id[%s]'%(item['need_filter'],item['id']),level=log.WARNING)
            if item['need_filter'] == 1 and (item['stat'] == 0 or item['stat'] == 1):
                item['stat'] = 2
                #print 'change stat to delete',key
                log.msg('change stat to delete id[%s]'%key,level=log.WARNING)
                self.delete_num += 1
                del item['_id']
                if self.uniq_key is None:
                    result = self.collection.insert(dict(item), safe=self.safe)
                else:
                    result = self.collection.update({self.uniq_key: item[self.uniq_key] }, { '$set': dict(item) },upsert=True, safe=self.safe)
                    #result =  self.collection.save(item)
        #更新same id
        for (key,value) in self.same_id_dict.items():
            log.msg('update same_id[%s],cur_id[%s]'%(key,value),level=log.WARNING)
            result = self.collection.update({self.uniq_key: key}, { '$set': {"same_id":value}},upsert=True, safe=self.safe)
        self.file.close()
        log.msg('total_num:%d,new_num:%d,indb_num:%d,same_num:%d,del_num:%d,crawl_each_site:%s,new_each_site:%s'%(self.total_crawl_num,self.new_num,self.in_db_num,self.may_same_num,self.delete_num,self._dict_to_str(self.crawl_num_dict),self._dict_to_str(self.new_item_dict)),level=log.INFO)
    def _dict_to_str(self,dict):
        str = ''
        flag = False
        for (key,value) in dict.items():
            str = '%s|%s:%d'%(str,key,value)
            flag = True
        if flag:
            str = str[1:]
        return str
