__author__ = 'gaonan'
#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from selenium import webdriver
from ZSecKill.settings import START_URL,TIME_OUT
from scrapy import log
from selenium.common.exceptions import NoSuchElementException
from ZSecKill.items import ZseckillItem
import time
import hashlib
import datetime
class ZSecKillSpider(BaseSpider):
    name = "ZSecKillSpider"
    start_urls = START_URL
    #start_urls = ["http://www.amazon.cn/%E4%BF%83%E9%94%80-%E7%89%B9%E4%BB%B7/b/ref=cs_top_nav_gb27?ie=UTF8&node=42450071"]

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)

    def get_day_start_unix(self):
        cur_str = datetime.datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
        return int(time.mktime(time.strptime(cur_str,'%Y-%m-%d %H:%M:%S')))
    def get_day_end_unix(self):
        cur_str = datetime.datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
        return int(time.mktime(time.strptime(cur_str,'%Y-%m-%d %H:%M:%S'))) + 86400 - 1
    def get_element_by_id(self,container,id):
        try:
            item = container.find_element_by_id(id)
            return item
        except NoSuchElementException:
            return None
    def get_elements_by_id(self,container,id):
        try:
            item = container.find_elements_by_id(id)
            return item
        except NoSuchElementException:
            return None
    def get_elements_by_classname(self,container,name):
        try:
            item = container.find_elements_by_class_name(name)
            return item
        except NoSuchElementException:
            return None
    def get_element_by_classname(self,container,name):
        try:
            item = container.find_element_by_class_name(name)
            return item
        except NoSuchElementException:
            return None
    def get_element_by_path(self,container,path):
        try:
            item = container.find_element_by_xpath(path)
            return item
        except NoSuchElementException:
            return None
    def get_elements_by_path(self,container,path):
        try:
            item = container.find_elements_by_xpath(path)
            return item
        except NoSuchElementException:
            return None

    def get_item_type(self,item):
        if self.get_element_by_id(item,'dealTimeRemaining'):
            #正在出售的商品
            return 1
        elif self.get_element_by_id(item,'dealClosedMessage'):
            #交易结束的
            return 2
        elif self.get_element_by_classname(item,'ldupcomingtxt'):
            #即将开始交易
            return 3
        else:
            return 4
    def process_time(self,time_str):
        log.msg('process time %s'%(time_str),level=log.DEBUG)
        hour = int(time_str[0:2])
        min = int(time_str[5:7])
        sec = int(time_str[-3:-1])
        log.msg('process time %d-%d-%d'%(hour,min,sec),level=log.DEBUG)
        return int(time.time()) + 3600*hour + 60*min + sec
    def process_number(self,num_str):
        if '-' in num_str:
            num_str = num_str.split('-')[0]
        return filter(lambda ch:ch in '0123456789.', num_str)
    def process_link(self,link_str):
        cur_list = link_str.split('/')
        cur_str = ''
        for i in cur_list[:-1]:
            cur_str += (i + '/')
        return cur_str

    def process_current_item(self,item):
        try:
            prod = ZseckillItem()
            title_link_obj = self.get_element_by_id(item,"dealTitleLink")
            if not title_link_obj:
                log.msg('get title link error',level=log.WARNING)
                return None
            #prod['title'] = title_link_obj.get_attribute("title")
            #prod['link'] = title_link_obj.get_attribute("href")
            prod['link'] = self.process_link(title_link_obj.get_attribute("href"))
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            price_obj = self.get_element_by_id(item,"dealDealPrice")
            if not price_obj:
                log.msg('get price error %s'%prod['link'],level=log.WARNING)
                return None
            prod['cur_price'] = int(float(self.process_number(price_obj.text))*100)
            #int(float((price_obj.text)[1:])*100)
            discount_obj = self.get_element_by_id(item,"dealPercentOff")
            if not discount_obj:
                log.msg('get discount error %s'%prod['link'],level=log.WARNING)
                prod['discount'] = -1
            else:
                prod['discount'] = int(float(self.process_number(discount_obj.text))*10)
            #(discount_obj.text)[1:-2]
            if prod['discount'] != -1:
                prod['ori_price'] = int(prod['cur_price'] * 100 / float(prod['discount']))
            else:
                prod['ori_price'] = -1
            limit_obj = self.get_element_by_id(item,"dealTotalCouponsCount")
            if not limit_obj:
                log.msg('get limit error %s'%prod['link'],level=log.WARNING)
                prod['limit'] = 0
            else:
                log.msg('get limit %s'%self.process_number(limit_obj.text),level=log.DEBUG)
                prod['limit'] = int(self.process_number(limit_obj.text))
                #int((limit_obj.text)[4:])
            sale_percent = 0
            sale_obj = self.get_element_by_id(item,"dealPercentClaimed")
            if not sale_obj:
                log.msg('get sale error %s'%prod['link'],level=log.WARNING)
            else:
                sale_percent = int(self.process_number(sale_obj.text))
                log.msg('get sale %s'%self.process_number(sale_obj.text),level=log.DEBUG)
                #float((sale_obj.text)[0:-5])
            prod['sale_percent'] = sale_percent
            prod['sale'] = int(prod['limit'] * sale_percent / 100)
            left_time_obj = self.get_element_by_id(item,"dealTimeRemaining")
            if not left_time_obj:
                log.msg('get left time error %s'%prod['link'],level=log.WARNING)
                return None
            prod['display_time_end'] = self.process_time(left_time_obj.text)
            prod['actual_time_end'] = prod['display_time_end']
            prod['stat'] = 2
            return prod
        except Exception as e:
            log.msg('process current item exception happen:%s'%e,level=log.WARNING)
            return None
    def process_upcoming_item(self,item):
        try:
            prod = ZseckillItem()
            link_obj = self.get_element_by_path(item,'.//div[@id="dealImageContent"]/div/a')
            if not link_obj:
                log.msg('get link error',level=log.WARNING)
                return None
            #prod['link'] = link_obj.get_attribute("href")
            prod['link'] = self.process_link(link_obj.get_attribute("href"))
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            prod['cur_price'] = -1
            prod['discount'] = -1
            prod['ori_price'] = -1
            prod['limit'] = -1
            prod['sale'] = -1
            prod['sale_percent'] = -1
            left_time_obj = self.get_element_by_path(item,'.//div[@id="dealStateContent"]/div/span')
            if not left_time_obj:
                log.msg('get left time error %s'%prod['link'],level=log.WARNING)
                return None
            prod['display_time_begin'] = self.process_time(left_time_obj.text)
            prod['actual_time_begin'] = prod['display_time_begin']
            prod['display_time_end'] = self.get_day_end_unix()
            prod['actual_time_end'] = prod['display_time_end']
            prod['stat'] = 1
            return prod
        except Exception as e:
            log.msg('process upcoming item exception happen:%s'%e,level=log.WARNING)
            return None
    def process_missed_item(self,item):
        try:
            prod = ZseckillItem()
            title_link_obj = self.get_element_by_id(item,"dealTitleLink")
            if not title_link_obj:
                log.msg('get title link error')
                return None
            #prod['link'] = title_link_obj.get_attribute("href")
            prod['link'] = self.process_link(title_link_obj.get_attribute("href"))
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            prod['stat'] = 3
            return prod
        except Exception as e:
            log.msg('process missed item exception happen:%s'%e,level=log.WARNING)
            return None

    def parse_current_item(self,type):
        cur_num = 0
        total_num = 1
        item_list = []
        while (cur_num < total_num):
            total_num_obj = self.get_element_by_id(self.driver,"dealTotalPages")
            if not total_num_obj:
                log.msg('get total page_num for %s error'%type,level=log.WARNING)
                return None
            total_num = int(total_num_obj.text)
            log.msg('get total page_num for %s %d'%(type,total_num),level=log.DEBUG)
            cur_num_obj = self.get_element_by_id(self.driver,"dealCurrentPage")
            if not cur_num_obj:
                log.msg('get current num for %s error'%type,level=log.WARNING)
                return None
            cur_num = int(cur_num_obj.text)
            log.msg('get cur num for %s %d'%(type,cur_num),level=log.DEBUG)
            items = self.get_elements_by_classname(self.driver,"noTopMargin")
            if not items:
                log.msg('get itmes for %s error'%type,level=log.WARNING)
                return None
            for item in items:
                item_type = self.get_item_type(item)
                log.msg('type is %d for %s'%(item_type,type),level=log.DEBUG)
                if item_type == 1:
                    ret_prod = self.process_current_item(item)
                elif item_type == 2:
                    ret_prod = self.process_missed_item(item)
                elif item_type == 3:
                    ret_prod = self.process_upcoming_item(item)
                else:
                    continue
                if ret_prod:
                    item_list.append(ret_prod)
                    log.msg('process id:%s %s'%(ret_prod['id'],item.get_attribute("id")),level=log.DEBUG)
                    log.msg('process id:%s link:%s cur_num:%d type:%s'%(ret_prod['id'],ret_prod['link'],cur_num,type),level=log.DEBUG)
                else:
                    log.msg('process type:%s %d page error '%(type,cur_num),level=log.WARNING)
            next_page_obj = self.get_element_by_id(self.driver,"rightShovelBg")
            if not next_page_obj:
                log.msg('get next page obj for %s error'%type,level=log.WARNING)
                return None
            next_page_obj.click()
            #time.sleep(1)
        return item_list

    def parse(self, response):
        try:
            self.driver.get(response.url)
            selling_list = self.parse_current_item('selling')
            if selling_list:
                log.msg('selling list len %d'%len(selling_list),level=log.DEBUG)
                for item in selling_list:
                    yield Request(url=item['link'],dont_filter=True,callback=self.parse_item,meta={'prod':item})
            else:
                log.msg('selling list is empty',level=log.DEBUG)
            self.driver.execute_script("document.getElementById('upcoming_filter').click();")
            time.sleep(2)
            log.msg('process upcoming',level=log.WARNING)
            upcoming_list = self.parse_current_item('upcoming')
            if upcoming_list:
                log.msg('upcoming list len %d'%len(upcoming_list),level=log.DEBUG)
                for item in upcoming_list:
                    yield Request(url=item['link'],dont_filter=True,callback=self.parse_item,meta={'prod':item})
            else:
                log.msg('upcoming list is empty',level=log.DEBUG)
            self.driver.execute_script("document.getElementById('missed_filter').click();")
            time.sleep(2)
            log.msg('process missed',level=log.WARNING)
            missed_list = self.parse_current_item('missed')
            if missed_list:
                log.msg('missed list len %d'%len(missed_list),level=log.DEBUG)
                for item in missed_list:
                    yield Request(url=item['link'],dont_filter=True,callback=self.parse_item,meta={'prod':item})
            else:
                log.msg('missed list is empty',level=log.DEBUG)
        except Exception as e:
            log.msg('exception happen:%s'%e,level=log.WARNING)
        finally:
            self.driver.quit()
        # process upcoming
    def parse_item(self,response):
        hxs = HtmlXPathSelector(response)
        prod = response.meta['prod']
        title = hxs.select('//h1[@class="parseasinTitle"]/span/span/text()').extract()
        if title:
            prod['title'] = title[0]
        else:
            log.msg('error get title error id:%s stat:%d'%(prod['id'],prod['stat']),level=log.WARNING)
            return
        img_item = hxs.select('//div[@class="main-image-inner-wrapper"]/img/@src').extract()
        if img_item:
            prod['img'] = img_item[0]
        else:
            log.msg('error get img_item error id:%s stat:%d'%(prod['id'],prod['stat']),level=log.WARNING)
            return
        prod['source'] = 'Z秒杀'
        return prod



