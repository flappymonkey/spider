#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib
import sys
sys.path.append('../comm_lib')
from utils import get_one, get_one_string, get_attr, get_obj_attr, get_num, to_fen, get_pic_url, get_item_id, get_discount, UNKNOWN_NUM, UNLIMITED_NUM
import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import hashlib
from taobao_tejia.items import TaobaoTejiaItem
import socket

class TaobaoTejiaSpider(BaseSpider):
    name = "taobao_tejia"
    allowed_domains = ["tejia.taobao.com"]
    start_urls = [
    "http://tejia.taobao.com/ttt.htm"
    ]
    display_name = u'天天特价'

    def __init__(self):
        self.cg = utils.CategoryGet(['../tools/1', '../tools/2'])
        socket.setdefaulttimeout(60)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        h_li_array = hxs.select('//dl[@class="to-item"]')
        ret_items = []
        for h_li in h_li_array:
            xpath_list=[
                ['title', 'dd[@class="title"]/a/text()', 'string', None],
                ['url', 'dt/a/@href', 'string', None],
                ['img_url', 'dt/a/img/@src', 'string', None],
                ['left_goods', 'dt/span[@class="remain"]/em/text()', 'int', None],
                ['current_price', 'dd/strong/text()', 'get_float_str_to_fen', None],
                ['origin_price', 'dd/del/text()', 'get_float_str_to_fen', None],
                ['sale', 'dd/span/em/text()', 'int', None],
            ]
            attr_dict = get_attr(xpath_list, h_li)
            if not attr_dict:
                continue
            prod = TaobaoTejiaItem()
            prod['link'] = attr_dict['url']
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            prod['title'] = attr_dict['title']
            index = attr_dict['img_url'].find('_210x210.jpg')
            if index == -1:
                log.msg('failed to find out _210x210.jpg in img_url', level = log.ERROR)
                continue
            log.msg('img_url_cut ' + attr_dict['img_url'][0:index], level = log.DEBUG)
            #prod['img'] = utils.get_pic_url(utils.get_id(attr_dict['url']))
            prod['img'] = attr_dict['img_url'][0:index]
            pic_url, detail_url, baoyou, cid = utils.get_taobao_item_info(utils.get_id(attr_dict['url']))
            if not pic_url:
                log.msg('failed to get taobao item info', level = log.DEBUG)
                continue

            if not baoyou:
                log.msg('skip goods because not baoyou', level = log.DEBUG)
                continue
            #second_pic_url = utils.get_second_pic_url(utils.get_id(attr_dict['url']))
            #log.msg('second_pic_url ' + second_pic_url, level = log.DEBUG)
            origin_category_name, category_name = self.cg.get_cid_name(cid)
            log.msg('origin_category_name ' + origin_category_name + ' category_name ' + category_name + ' title ' + attr_dict['title'] + ' url ' + attr_dict['url'], level = log.DEBUG)
            prod['ori_price'] = attr_dict['origin_price']
            prod['cur_price'] = attr_dict['current_price']
            prod['discount'] = utils.get_discount(attr_dict['current_price'], attr_dict['origin_price'])
            prod['sale'] = utils.UNKNOWN_NUM
            prod['sale_percent'] = utils.UNKNOWN_NUM
            prod['limit'] = utils.UNLIMITED_NUM
            prod['display_time_begin'] = int(time.time())
            prod['display_time_end'] = utils.get_default_end_time()
            left_goods = utils.get_left_goods(utils.get_id(attr_dict['url']))
            log.msg('left_goods ' + str(left_goods), level = log.DEBUG)
            if left_goods > 0:
                prod['stat'] = utils.BEGIN
            else:
                prod['stat'] = utils.END
                prod['display_time_end'] = int(time.time())
            prod['source'] = self.display_name
            prod['origin_category_name'] = origin_category_name
            prod['category_name'] = category_name
            ret_items.append(prod)
        return ret_items
