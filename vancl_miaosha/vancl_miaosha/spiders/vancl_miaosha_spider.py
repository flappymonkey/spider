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
import sys
sys.path.append('../comm_lib')
from utils import get_one, get_one_string, get_attr, get_obj_attr, get_num, to_fen, get_discount
from vancl_miaosha.items import VanclMiaoshaItem
import datetime
import utils

class VanclMiaoshaSpider(BaseSpider):
    name = "vancl_miaosha"
    allowed_domains = ["vancl.com"]
    start_urls = [
    "http://tuan.vancl.com/SecKill"
    ]
    display_name = u'凡客'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        h_div = get_one(hxs.select('//body/div[@id="bodydiv"]/div[@class="main_content"]/div/div[@class="left_cont"]/div[@id="msnew"]/div[@class="msnew_infobar"]'))
        xpath_list_div = [
            ['start_time_str', 'div[@class="msnew_infotitle"]/p[@class="msinfotitle_left02"]/text()', 'strip', None], 
            ['from_time', 'span[@class="CountDown"]/@fr', 'int', None], 
            ['to_time', 'span[@class="CountDown"]/@to', 'int', None], 
        ]
        if not h_div:
            self.log('no page to parse', level = log.WARNING)
            return
        attr_dict = get_attr(xpath_list_div, h_div)
        start_time_str = str(datetime.datetime.now().date()) + " " + attr_dict['start_time_str'] 
        print 'start_time_str ' + start_time_str.encode('utf8')
        display_time_begin = int(datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
        print 'display_time_begin ' + str(display_time_begin)
        cost_seconds = ((attr_dict['to_time'] - attr_dict['from_time']) / 1000)
        print 'cost_seconds ' + str(cost_seconds)
        display_time_end = display_time_begin + cost_seconds
        print 'display_time_end ' + str(display_time_end)
        
        h_li_array = hxs.select('//body/div[@id="bodydiv"]/div[@class="main_content"]/div/div[@class="left_cont"]/div[@id="msnew"]/div[@class="msnew_infobar"]/ul[@id="ms_tuanlist"]/li')
        print "len " + str(len(h_li_array))

        xpath_list = [
            ['img_url', 'div[@class="pic"]/a/img/@src', 'string', None],
            ['title', 'div[@class="info"]/span/a[@target="_blank"]/@title', 'string', None],
            ['url', 'div[@class="info"]/span/a[@target="_blank"]/@href', 'string', None],
            ['origin_price', 'div[@class="info"]/span[@class="gray6"]/text()', 'get_float_str_to_fen', None],
            ['current_price', 'div[@class="info"]/span[@class="redf16"]/text()', 'get_float_str_to_fen', None],
            ['sale_info', 'div[@class="info"]/span[@class="red94"]/text()', 'string', None],
        ]
        ret_items = []
        for h_li in h_li_array:
            attr_dict = get_attr(xpath_list, h_li)
            if attr_dict['url'][0] == '/':
                attr_dict['url'] = 'http://tuan.vancl.com' + attr_dict['url'] 

            limit = get_num(attr_dict['sale_info'].split(' ')[0])
            left = get_num(attr_dict['sale_info'].split(' ')[1])
            sale = limit - left
            print 'limit ' + str(limit) + " left " + str(left)
            prod = VanclMiaoshaItem()
            prod['link'] = attr_dict['url']
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            prod['title'] = attr_dict['title']
            prod['img'] = attr_dict['img_url']
            prod['ori_price'] = attr_dict['origin_price']
            prod['cur_price'] = attr_dict['current_price']
            prod['discount'] = get_discount(attr_dict['origin_price'], attr_dict['current_price'])
            #TODO
            prod['stat'] = utils.BEGIN
            prod['sale'] = sale
            prod['sale_percent'] = sale * 100 / limit
            prod['display_time_begin'] = display_time_begin
            prod['display_time_end'] = display_time_end
            #prod['actual_time_begin'] = start_time
            #prod['actual_time_end'] = start_time
            prod['limit'] = limit
            prod['source'] = self.display_name
            ret_items.append(prod)

        return ret_items
