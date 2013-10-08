#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from Smzdm.items import SmzdmItem
from urllib import unquote
from urllib import quote
import Smzdm.settings
import re
import hashlib
import datetime

from scrapy import log

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SmzdmSpider(BaseSpider):
    name = "SmzdmSpider"
    start_urls = Smzdm.settings.START_URL
    dr = re.compile(r'<[^>]+>',re.S)
    scrapy_mode = 2
    max_items = Smzdm.settings.MAX_ITEM_NUM
    max_time_diff = Smzdm.settings.CUT_TIME
    cur_date=datetime.datetime.now()

    def __init__(self,mode = 2):
        '''
        0: 没有抓取限制
        1: 以抓取条数为限制
        2: 以时间差为限制，既和当前时间相差的秒数，对于没有配置时间的垃圾网站则使用条数限制,默认值
        '''
        self.scrapy_mode = int(mode)
    def _get_link(self,link):
        link = unquote(unquote(link))
        split_list = link.split('http://')
        if split_list:
            link = 'http://' + split_list[-1]
        return quote(link)
        #return link

    def _process_url(self,src_url,pre):
        if not 'http://' in src_url:
            return pre + src_url
        else:
            return src_url

    def _get_time_diff(self,t_str,time_format):

        if cmp(time_format,'%m-%d %H:%M') == 0:
           t_str = str(self.cur_date.year) + '-' + t_str + ':' + str(self.cur_date.second)
           time_format = '%Y-%m-%d %H:%M:%S'
        if cmp(time_format,'NONE') == 0:
            return self.cur_date.strftime('%Y-%m-%d %H:%M:%S'),0
        com_date = datetime.datetime.strptime(t_str,time_format)
        return com_date.strftime('%Y-%m-%d %H:%M:%S'),(self.cur_date-com_date).seconds + (self.cur_date-com_date).days*86400

    def parse(self,response):
        item_nums = 0
        if 'item_num' in response.meta:
            item_nums = response.meta['item_num']
        if 'cur_name' in response.meta:
            CUR_NAME = response.meta['cur_name']
        else:
            if not response.url in Smzdm.settings.URL_TO_NAME:
                log.msg('start url:%s is unknown'% response.url,level=log.WARNING)
                return
            CUR_NAME = Smzdm.settings.URL_TO_NAME[response.url]
        log.msg('current process name is %s'% CUR_NAME,level=log.DEBUG)
        for (name,path_dict) in Smzdm.settings.PATH_CONFIG.items():
            if not CUR_NAME in path_dict:
                #print CUR_NAME,name
                log.msg('no config[%s] for name[%s]'%(name,CUR_NAME),level=log.CRITICAL)
                return
        time_format = Smzdm.settings.PATH_CONFIG['PUB_TIME_FORMAT'][CUR_NAME]
        #need_filter = 1
        #if cmp(time_format,'NONE') == 0:
        #   log.msg('current format is %s, no need filter'% time_format,level=log.DEBUG)
        #    need_filter = 0
        hxs = HtmlXPathSelector(response)
        #contents = hxs.select('//div[@class="perContentBox "]')
        log.msg('process model is %d'% self.scrapy_mode,level=log.DEBUG)
        contents = hxs.select(Smzdm.settings.PATH_CONFIG['MAIN_PATH'][CUR_NAME])
        if not contents:
            log.msg('[%s] get main content error,path[%s]'% (CUR_NAME,Smzdm.settings.PATH_CONFIG['MAIN_PATH'][CUR_NAME]),level=log.WARNING)
            return
        for content in contents:
            #titles = content.select('div/h2[@class="con_title"]/a/@title').extract()
            if self.scrapy_mode == 1 or (cmp(time_format,'NONE') == 0 and self.scrapy_mode != 0):
                if item_nums >= self.max_items:
                    log.msg('[%s] process items:%d more than setting %d'% (CUR_NAME,item_nums,self.max_items),level=log.WARNING)
                    return
            title_list = []
            for cur_title_path in Smzdm.settings.PATH_CONFIG['TITLE_PATH'][CUR_NAME]:
                titles = content.select(cur_title_path).extract()
                title_list += titles
            if not title_list:
                log.msg('[%s] get title error,path[%s]'% (CUR_NAME,Smzdm.settings.PATH_CONFIG['TITLE_PATH'][CUR_NAME]),level=log.WARNING)
                continue
            #past_time = content.select('div[@class="dateTime"]/text()').extract()

            t_diff = 0
            com_date = ''
            if cmp(time_format,'NONE') == 0:
                (com_date,t_diff) = self._get_time_diff('NONE','NONE')
            else:
                past_time = content.select(Smzdm.settings.PATH_CONFIG['PUB_TIME_PATH'][CUR_NAME]).extract()
                if not past_time:
                    log.msg('[%s] get past time error,path[%s]'% (CUR_NAME,Smzdm.settings.PATH_CONFIG['PUB_TIME_PATH'][CUR_NAME]),level=log.WARNING)
                    continue
                (com_date,t_diff) = self._get_time_diff(past_time[0],time_format)
            log.msg('com_data[%s],time diff[%d]'% (com_date,t_diff),level=log.DEBUG)
            #print self.scrapy_mode,t_diff,self.max_time_diff
            if self.scrapy_mode == 2:
                if t_diff > self.max_time_diff:
                    log.msg('[%s] time diff[%d] more than setting [%d]'% (CUR_NAME,t_diff,self.max_time_diff),level=log.WARNING)
                    #print "get",com_date,t_diff,self.max_time_diff
                    return
            #判断第一层是否有店铺
            source_item = []
            sources = content.select(Smzdm.settings.PATH_CONFIG['SOURCE_PATH'][CUR_NAME]).extract()
            if sources:
                source_item.append(sources[0])
            #urls = content.select('div/h2[@class="con_title"]/a/@href').extract()
            urls = content.select(Smzdm.settings.PATH_CONFIG['CONTENT_URL'][CUR_NAME]).extract()
            if urls:
                #yield Request(url=Smzdm.settings.PATH_CONFIG['PRE_URL'][CUR_NAME] + urls[-1],callback=self.parse_desc,meta={'title':title,'p_data':com_data,'crawl_s':Smzdm.settings.PATH_CONFIG['NAME_TO_SHOW'][CUR_NAME],'crawl_name':CUR_NAME,'sor_item':source_item})
                temp_use_url = self._process_url(urls[-1],Smzdm.settings.PATH_CONFIG['NAME_TO_PRE'][CUR_NAME])
                #print CUR_NAME,urls[-1],temp_use_url
                log.msg('[%s] content url is [%s] source url is [%s]'%(CUR_NAME,temp_use_url,urls[-1]),level=log.DEBUG)
                log.msg('[%s] request for [%s],title:%s,p_data:%s,sor_item:%s'%(CUR_NAME,temp_use_url,title_list,com_date,source_item),level=log.DEBUG)
                yield Request(url=temp_use_url,callback=self.parse_desc,meta={'title':title_list,'p_data':com_date,'crawl_s':Smzdm.settings.PATH_CONFIG['NAME_TO_SHOW'][CUR_NAME],'crawl_name':CUR_NAME,'sor_item':source_item})
            item_nums += 1
        #next_url = hxs.select('//a[@class="pagedown"]/@href').extract()
        next_url = hxs.select(Smzdm.settings.PATH_CONFIG['NEXT_PAGE'][CUR_NAME]).extract()
        if next_url:
            #print 'com here',response.url,next_url[Smzdm.settings.PATH_CONFIG['NEXT_PAGE_INDEX'][CUR_NAME]],CUR_NAME
            temp_use_url = self._process_url(next_url[Smzdm.settings.PATH_CONFIG['NEXT_PAGE_INDEX'][CUR_NAME]],Smzdm.settings.PATH_CONFIG['NAME_TO_PRE'][CUR_NAME])
            log.msg('[%s] get next page source url[%s],get url[%s]'%(CUR_NAME,next_url[Smzdm.settings.PATH_CONFIG['NEXT_PAGE_INDEX'][CUR_NAME]],temp_use_url),level=log.WARNING)
            log.msg('[%s] current item num[%d]'%(CUR_NAME,item_nums),level=log.DEBUG)
            yield Request(url=temp_use_url,callback=self.parse,meta={'cur_name':CUR_NAME,'item_num':item_nums})
            #yield Request(url=Smzdm.settings.PATH_CONFIG['NEXT_PAGE_PRE'][CUR_NAME] + next_url[Smzdm.settings.PATH_CONFIG['NEXT_PAGE_INDEX'][CUR_NAME]],callback=self.parse,meta={'cur_name':CUR_NAME,'item_num':item_nums})
        else:
            log.msg('[%s] get next page error,path[%s]'%(CUR_NAME,Smzdm.settings.PATH_CONFIG['NEXT_PAGE'][CUR_NAME]),level=log.WARNING)
    def parse_desc(self,response):
        prod = SmzdmItem()
        link_dict={}
        desc_list=[]
        img_list = []
        go_link_list = []
        desc_items = []

        CUR_NAME = response.meta['crawl_name']
        prod['source_url'] = response.url
        prod['id'] = hashlib.md5(response.url).hexdigest().upper()

        hxs = HtmlXPathSelector(response)
        #main_items = hxs.select('//div[@class="perContentBox"]')
        main_items = hxs.select(Smzdm.settings.PATH_CONFIG['DESC_MAIN_PATH'][CUR_NAME])
        if len(main_items) != 1:
            log.msg('[%s] get content error,num[%d] more than 1'%(CUR_NAME,len(main_items)),level=log.WARNING)
        main_item = main_items[0]

        for cur_path in Smzdm.settings.PATH_CONFIG['DESC_PATH'][CUR_NAME]:
            desc_items =  desc_items + main_item.select(cur_path)

        for desc_item in desc_items:
            #cur_str = desc_item.extract().encode('utf-8')
            cur_str = desc_item.extract()
            if not '<script' in cur_str:
                desc_str = self.dr.sub('',cur_str)
                if len(desc_str) > 2:
                    desc_list.append(desc_str)
            #href_items = desc_item.select('.//a/')
            href = desc_item.select(Smzdm.settings.PATH_CONFIG['DESC_LINK_URL'][CUR_NAME]).extract()
            href_desc = desc_item.select(Smzdm.settings.PATH_CONFIG['DESC_LINK_CONTENT'][CUR_NAME]).extract()
            h_len = len(href_desc)
            if len(href_desc) > len(href):
                h_len = len(href)
            for i in range(0,h_len):
                #link_dict[href_desc[i].encode('utf-8')] = href[i]
                #print i,href_desc[i],len(href_desc)
                #print i,href[i],len(href)
                link_dict[href_desc[i]] = href[i]
            img_list += desc_item.select(Smzdm.settings.PATH_CONFIG['DESC_IMG_PATH'][CUR_NAME]).extract()
        img_list += main_item.select(Smzdm.settings.PATH_CONFIG['IMG_PATH'][CUR_NAME]).extract()

        for cur_path in Smzdm.settings.PATH_CONFIG['GO_LINK_PATH'][CUR_NAME]:
            go_link_list += main_item.select(cur_path).extract()
        ret_items = []
        i = 0

        for go_link in go_link_list:
            #print  CUR_NAME,prod['id'],Smzdm.settings.PATH_CONFIG['GO_LINK_PRE'][CUR_NAME] + go_link
            temp_use_url = self._process_url(go_link,Smzdm.settings.PATH_CONFIG['NAME_TO_PRE'][CUR_NAME])
            #print CUR_NAME,go_link,temp_use_url
            #print 'go link',prod['id'],temp_use_url
            ret_items.append(Request(url=temp_use_url,dont_filter=True,callback=self.parse_link,meta={'id':prod['id'],'desc':str(i),'flag':2}))
            i += 1
        prod['title'] = response.meta['title']
        prod['desc'] = desc_list
        #prod['desc_link'] = link_dict
        prod['img'] = img_list
        #cur_time = main_item.select('//div[@class="dateTime"]/text()').extract()
        #if cur_time:
        #    prod['pub_time'] = cur_time[0]
        prod['pub_time'] = response.meta['p_data']
        prod['cat'] = []

        #cats = main_item.select('//div[@class="classified"]/a/text()').extract()
        cats = main_item.select(Smzdm.settings.PATH_CONFIG['CAT_PATH'][CUR_NAME]).extract()
        for cur_cat in cats:
            #prod['cat'].append(cur_cat.encode('utf-8'))
            prod['cat'].append(cur_cat)
        #prod['cat'] = main_item.select('//div[@class="classified"]/a/text()').extract()
        prod['source'] = []
        sources = main_item.select(Smzdm.settings.PATH_CONFIG['SOURCE_PATH'][CUR_NAME]).extract()
        if sources:
            for cur_source in sources:
                prod['source'].append(cur_source)
        elif response.meta['sor_item']:
            prod['source'] = response.meta['sor_item']

        for (desc,link) in link_dict.items():
            temp_use_url = self._process_url(link,Smzdm.settings.PATH_CONFIG['NAME_TO_PRE'][CUR_NAME])
            #print CUR_NAME,link,temp_use_url
            #print 'desc link',prod['id'],desc,temp_use_url
            ret_items.append(Request(url=temp_use_url,callback=self.parse_link,dont_filter=True,meta={'id':prod['id'],'desc':desc,'flag':1}))
        #print prod['source_url'],prod['id'],prod['title'],prod['desc'],prod['desc_link'],prod['pub_time'],prod['img'],prod['cat'],prod['source']
        prod['flag'] = 0
        prod['worth_num'] = 0
        #w_score = main_item.select('//div[@class="worth_1"]/a/text()').extract()
        w_score = main_item.select(Smzdm.settings.PATH_CONFIG['WORTH_SCORE_PATH'][CUR_NAME]).extract()
        if w_score:
            prod['worth_num'] = w_score[0]
        prod['bad_num'] =0
        #b_score = main_item.select('//div[@class="worth_3"]/a/text()').extract()
        b_score = main_item.select(Smzdm.settings.PATH_CONFIG['BAD_SCORE_PATH'][CUR_NAME]).extract()
        if b_score:
            prod['bad_num'] = b_score[0]
        prod['crawl_source'] = response.meta['crawl_s']
        prod['stat'] = 0
        prod['need_filter'] = Smzdm.settings.PATH_CONFIG['NEED_FILTER'][CUR_NAME]
        prod['same_id'] = 'NONE'
        ret_items.append(prod)
        log.msg('[%s] get item %r'%(CUR_NAME,prod),level=log.DEBUG)
        return ret_items
    def parse_link(self,response):
        prod = SmzdmItem()
        prod['id'] = response.meta['id']
        prod['link_desc'] = response.meta['desc']
        prod['link'] = self._get_link(response.url)
        prod['flag'] = response.meta['flag']
        log.msg('get url %r'%prod,level=log.DEBUG)
        #print 'aa',response.meta['id'],response.url,unquote(unquote(response.url)),prod['link']
        return prod
