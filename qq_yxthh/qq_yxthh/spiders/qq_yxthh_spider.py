#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from qq_yxthh.items import QqYxthhItem
import time
import hashlib
import decimal
import re
import sys
sys.path.append('../comm_lib')
from utils import get_one, get_one_string, get_attr, get_obj_attr, get_num, to_fen, get_pic_url, get_item_id, get_discount, UNKNOWN_NUM, UNLIMITED_NUM
import time
import utils
import socket

debug = False
print_url = False

class QQYxthhSpider(BaseSpider):
    name = "qq_yxthh"
    allowed_domains = ["yixun.com", "event.yixun.com", "sale.yixun.com"]
    start_urls = [
    "http://sale.yixun.com/nightmarket.html?YTAG=1.100000804"
    ]
    display_name = u'易迅'

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        socket.setdefaulttimeout(60)

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
    def get_elements_by_tagname(self,container,tag):
        try:
            item = container.find_elements_by_tag_name(tag)
            return item
        except NoSuchElementException:
            return None
    def get_element_by_classname(self,container,name):
        try:
            item = container.find_elements_by_class_name(name)
            return item
        except NoSuchElementException:
            return None

    def parse(self, response):
        if not utils.get_url_by_browser(self.driver, response.url):
            return
        xpath='//body/div[@id="container"]/div[@class="page_nm"]/div[@class="mod mod_sp"]/div[@class="mod_sp_inner"]/div[@class="bd"]/ul[@id="red_pro_list"]/li'
        li_obj_array = self.driver.find_elements_by_xpath(xpath)
        ret_items = []
        for li_obj in li_obj_array:
            xpath_list = [
                ['title', 'div[@class="inner"]/div[@class="name"]/a', 'text()', 'string', None],
                ['url', 'div[@class="inner"]/div[@class="pic_wrap"]/a', 'href', 'string', None],
                ['img_url', 'div[@class="inner"]/div[@class="pic_wrap"]/a/img', 'src', 'string', None],
                ['origin_price', 'div[@class="inner"]/div[@class="price_stock"]/p[@class="price"]', 'text()', 'get_float_str_to_fen', None],
                ['current_price', 'div[@class="inner"]/div[@class="action"]/dl/dd', 'text()', 'get_float_str_to_fen', None],
                ['display_time_begin', 'div[@class="inner"]/div[@class="action"]/a', 'starttime', 'int', None],
                ['kucun_percent', 'div[@class="inner"]/div[@class="price_stock"]/p[@class="yx_stock"]/span[@class="yx_stock_less"]/span[@class="yx_stock_inner"]', 'style', 'get_num', None],
                ['classname', 'div[@class="inner"]/div[@class="action"]/a', 'class', 'string', None],
            ]
            attr_dict = get_obj_attr(xpath_list, li_obj)
            if not attr_dict:
                continue
            prod = QqYxthhItem()
            prod['link'] = attr_dict['url']
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            prod['title'] = attr_dict['title']
            prod['img'] = attr_dict['img_url']
            prod['ori_price'] = attr_dict['origin_price']
            prod['cur_price'] = attr_dict['current_price']
            prod['discount'] = get_discount(attr_dict['current_price'], attr_dict['origin_price'])
            if attr_dict['classname'] == 'go go_remind':
                prod['stat'] = utils.NOT_BEGIN
            elif attr_dict['classname'] == 'go':
                prod['stat'] = utils.BEGIN
            else:
                #TODO
                self.log('unknown state ' + attr_dict['classname'], level = log.ERROR)
            prod['sale'] = utils.UNKNOWN_NUM
            prod['sale_percent'] = 100 - attr_dict['kucun_percent']
            prod['display_time_begin'] = attr_dict['display_time_begin']
            prod['display_time_end'] = utils.get_default_end_time()
            #prod['display_time_end'] = start_time
            #prod['actual_time_begin'] = start_time
            #prod['actual_time_end'] = start_time
            prod['limit'] = utils.UNLIMITED_NUM
            prod['source'] = self.display_name
            origin_category_name = u'数码/家电'
            category_name = u'数码/家电'
            prod['origin_category_name'] = origin_category_name
            prod['category_name'] = category_name
            ret_items.append(prod)
            log.msg('origin_category_name ' + origin_category_name + ' category_name ' + category_name + ' title ' + attr_dict['title'] + ' url ' + attr_dict['url'], level = log.DEBUG)

        return ret_items

