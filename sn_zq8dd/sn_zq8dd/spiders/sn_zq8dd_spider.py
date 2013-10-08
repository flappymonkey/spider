#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib
import hashlib
from datetime import datetime, date, time, timedelta
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
sys.path.append('../comm_lib')
from utils import get_one, get_one_string, get_attr, get_obj_attr, get_num, to_fen
from sn_zq8dd.items import SnZq8DdItem
import time
import utils

debug = False
print_url = False

def has_left_time(attr_dict):
    attr_list = ['left_hour', 'left_minute', 'left_second']
    for attr in attr_list:
        if not attr_dict.has_key(attr):
            return False
        if attr_dict[attr] == '-':
            return False
        if attr_dict[attr] == '':
            return False
    return True

class SnZq8DdSpider(BaseSpider):
    name = "sn_zq8dd"
    allowed_domains = ["suning.cn", "suning.com"]
    start_urls = [
    "http://image.suning.cn/images/advertise/001/130506zqbdd/index.html"
    #"http://www.suning.com/emall/prd_10052_10051_-7_12068417_.html"
    ]
    display_name = u'苏宁易购'
    
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)

    def parse_goods(self, response):
        #hxs = HtmlXPathSelector(response)
        #h_div = get_one(hxs.select('//body/div[@class="product-main-content w fix"]'))
        if not utils.get_url_by_browser(self.driver, response.url):
            return
        time.sleep(1)
        div_obj = self.driver.find_element_by_xpath('//body/div[@class="product-main-content w fix"]')

        #file = open("b.html", 'w')
        #file.write(response._body)
        #file.close()
        print "parse_goods " + response._url
        xpath_list = [
            ['title', 'div[@class="product-summary"]/div[@class="product-main-title"]/h1[@class="wb"]', 'title', 'string', None],
            ['img_url', 'div[@class="product-gallery"]/div[@class="product-preview-box pr"]/div[@class="product-preview"]/a[@class="view-img"]/img', 'src', 'string', None],
            ['origin_price', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/ul[@class="product-info-type fix cl"]/li[@class="fix sn-price"]/del[@class="arial gray"]/em', 'text()', 'to_fen', None],
            ['origin_price2', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/ul[@class="product-info-type fix cl"]/li[@id="netPriceBox"]/span[@id="netPrice"]/em', 'text()', 'to_fen', None],
            ['current_price', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/ul[@class="product-info-type fix cl"]/li[@class="fix sn-price"]/span[@class="main-price snPrice"]/em', 'text()', 'to_fen', None],
            ['current_price2', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/ul[@class="product-info-type fix cl"]/li[@id="allcuxiao"]/div[@id="promotion_tab_box"]/ul[@id="isquickBuyBox"]/li/span[@class="snPrice"]/em', 'text()', 'to_fen', None],
            ['left_goods', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/div[@class="pro-choose-box fix cl qiang mt10"]/dl[@class="fix rest-num"]/dd/span[@class="gray9"]', 'text()', 'get_num', None],
            ['left_hour', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/div[@class="pro-choose-box fix cl qiang mt10"]/dl[@id="endTimeDIV"]/dd/div[@class="clockbox"]/span[@class="hour"]', 'text()', 'string', None],
            ['left_minute', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/div[@class="pro-choose-box fix cl qiang mt10"]/dl[@id="endTimeDIV"]/dd/div[@class="clockbox"]/span[@class="minute"]', 'text()', 'string', None],
            ['left_second', 'div[@class="product-summary"]/div[@class="product-info-box pr"]/div[@class="pro-choose-box fix cl qiang mt10"]/dl[@id="endTimeDIV"]/dd/div[@class="clockbox"]/span[@class="second"]', 'text()', 'string', None],
        ]
        attr_dict = get_obj_attr(xpath_list, div_obj)
        if attr_dict.has_key('origin_price') and attr_dict.has_key('current_price'):
            origin_price = attr_dict['origin_price']
            current_price = attr_dict['current_price']
        elif attr_dict.has_key('origin_price2') and attr_dict.has_key('current_price2'):
            origin_price = attr_dict['origin_price2']
            current_price = attr_dict['current_price2']
        elif attr_dict.has_key('origin_price2') and not attr_dict.has_key('current_price2'):
            origin_price = attr_dict['origin_price2']
            current_price = origin_price
            origin_price = -1
            
        prod = SnZq8DdItem()
        prod['link'] = response._url 
        prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
        prod['title'] = attr_dict['title']
        prod['img'] = attr_dict['img_url']
        prod['ori_price'] = origin_price
        prod['cur_price'] = current_price
        if current_price >= 0 and origin_price > 0:
            prod['discount'] = utils.get_discount(current_price, origin_price)
        else:
            prod['discount'] = utils.UNKNOWN_NUM
        if attr_dict.has_key('left_goods') and attr_dict['left_goods']:
            prod['left_goods'] = attr_dict['left_goods']
        #TODO
        prod['stat'] = 2
        prod['sale'] = -1
        prod['sale_percent'] = -1
        prod['display_time_begin'] = int(datetime.now().strftime("%s"))
        if has_left_time(attr_dict):
            end_time = datetime.now() + timedelta(hours = int(attr_dict['left_hour']), minutes = int(attr_dict['left_minute']), seconds = int(attr_dict['left_second']))
            print 'end_time ' + str(end_time)
            prod['display_time_end'] = int(end_time.strftime("%s"))
        else:
            prod['display_time_end'] = utils.get_default_end_time()
        #prod['actual_time_begin'] = start_time
        #prod['actual_time_end'] = start_time
        limit = 0
        prod['limit'] = limit
        prod['source'] = self.display_name
        return prod

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        h_area_array = hxs.select('//body/div[@class="bodyBG"]/div[@class="warp"]/div[@class="main"]/div[@class="content"]/div[@class="general"]/map[@id="Map2"]/area')
        for h_area in h_area_array:
            url = get_one(h_area.select('@href').extract())
            if len(url) > 4 and url[:4] == 'http':
                print 'url ' + url
                yield Request(url = url, callback = self.parse_goods)
                if debug:
                    break
