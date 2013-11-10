#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from taobao_jhs.items import TaobaoJhsItem
import hashlib
from datetime import datetime, date, time, timedelta
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

def get_left_ms(h):
    h_div_array = h.select('div')
    for h_div in h_div_array:
        class_name = get_one(h_div.select('@class').extract())
        if class_name.find('title-bar') != -1 and class_name.find('current') != -1:
            left_ms_str = get_one(h_div.select('span[@class="point-watch"]/@data-total').extract())
            if not left_ms_str:
                return None
            return int(left_ms_str)
    return None

class TaobaoJhsSpider(BaseSpider):
    name = "taobao_jhs"
    allowed_domains = ["ju.taobao.com"]
    start_urls = [
    "http://ju.taobao.com/tg/point_list.htm?spm=608.2214381.0.0.u3c3Hj"
    ]
    display_name = u'聚划算'

    def __init__(self):
        self.cg = utils.CategoryGet(['../tools/1', '../tools/2'])
        socket.setdefaulttimeout(60)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        h_li_array = hxs.select('//body/div[@class="wrapper"]/div[@id="page"]/div[@id="content"]/div[@class="point-nav-box"]/div[@class="point-nav_new J_PointNav"]/div[@id="J_timeline"]/div[@class="timeline_scroll"]/ul[@class="clearfix"]/li')
        ret_items = []
        for h_li in h_li_array:
            xpath_list = [
                ['classname', '@class', 'string', None],
                ['url', 'a/@href', 'string', None],
                ['data-point', '@data-point', 'int', None],
            ]
            attr_dict = get_attr(xpath_list, h_li)
            if not attr_dict:
                continue
            ret_items.append(Request(url = attr_dict['url'], callback=self.parse_one_day, meta={'data-point':attr_dict['data-point']}))
        return ret_items

    def parse_one_day(self, response, is_today = True):
        hxs = HtmlXPathSelector(response)
        ret_items = []
        if is_today:
            h_div_array = hxs.select('//body/div[@class="wrapper"]/div[@id="page"]/div[@id="content"]/div[@class="point-list "]/div[@data-type="td"]')
        else:
            h_div_array = hxs.select('//body/div[@class="wrapper"]/div[@id="page"]/div[@id="content"]/div[@class="point-list "]/div[@data-type="tm"]')
        log.msg("len " + str(len(h_div_array)), level=log.DEBUG)
        for h_div in h_div_array:
            data_point = get_one_string(h_div.select('@data-point').extract())
            if is_today:
                start_time_str = str(datetime.now().date()) + " " + data_point + ":00:00"
            else:
                start_time_str = str((datetime.now() + timedelta(days = 1)).date()) + " " + data_point + ":00:00"
            start_time = int(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
            end_time = None
            left_ms = get_left_ms(h_div)
            if left_ms:
                end_time = int(time.time() + left_ms/1000)
                log.msg('start_time ' + str(start_time) + ' end_time ' + str(end_time), level=log.DEBUG)

            h_li_array = h_div.select('div[@class="ju-itemlist J_JuHomeList"]/ul[@class="clearfix"]/li')  
            for h_li in h_li_array:
                xpath_list = [
                    ['img_url1', 'a/img/@src', 'string', None],
                    ['img_url2', 'a/img/@data-ks-lazyload', 'string', None],
                    ['url', 'a/@href', 'string', None],
                    ['title', 'a/@aria-label', 'string', None],
                    ['current_price_yuan', 'a/div[@class="item-prices"]/span[@class="price"]/em/text()', 'string', None],
                    ['current_price_fen', 'a/div[@class="item-prices"]/span[@class="price"]/text()', 'string', None],
                    ['discount', 'a/div[@class="item-prices"]/div[@class="dock"]/span[@class="discount"]/em/text()', 'get_discount_int', None],
                    ['limit', 'a/div[@class="item-prices"]/div[@class="dock"]/span[@class="limit-num"]/text()', 'get_num', UNLIMITED_NUM],
                    ['origin_price', 'a/div[@class="item-prices"]/div[@class="dock"]/del[@class="orig-price"]/text()', 'get_float_str_to_fen', None],
                    ['sale', 'a/div[@class="item-prices"]/span[@class="sold-num"]/em/text()', 'int', UNKNOWN_NUM],
                    ['will', 'a/div[@class="item-prices"]/span[@class="sold-num"]/text()', 'strip', None],
                    ['li_classname', '@class', 'string', None],
                ]
                attr_dict = get_attr(xpath_list, h_li)
                if not attr_dict:
                    continue
                log.msg("start = " + str(start_time), level=log.DEBUG)
                if not attr_dict.has_key('will'):
                    attr_dict['sale'] = UNKNOWN_NUM
                elif attr_dict['will'] != u'人已买':
                    attr_dict['sale'] = UNKNOWN_NUM

                sale_percent = -1
                if attr_dict['limit'] != UNLIMITED_NUM and attr_dict['sale'] != UNKNOWN_NUM:
                    sale_percent = int(attr_dict['sale'] * 100 / attr_dict['limit'])
                    log.msg("sale_percent = " + str(sale_percent) + "%", level=log.DEBUG)
                
                if attr_dict.has_key('img_url1'):
                    img_url = attr_dict['img_url1']
                else:
                    img_url = attr_dict['img_url2']
                img_url, detail_url, baoyou, cid = utils.get_taobao_item_info(get_item_id(attr_dict['url']))
                origin_category_name, category_name = self.cg.get_cid_name(cid)
                log.msg('origin_category_name ' + origin_category_name + ' category_name ' + category_name + ' title ' + attr_dict['title'] + ' url ' + attr_dict['url'], level = log.DEBUG)
                log.msg("img_url = " + str(img_url), level=log.DEBUG)

                if not baoyou:
                    log.msg('skip goods because not baoyou', level = log.DEBUG)
                    continue

                if attr_dict.has_key('current_price_fen'):
                    current_price = to_fen(attr_dict['current_price_yuan'] + attr_dict['current_price_fen'])
                else:
                    current_price = to_fen(attr_dict['current_price_yuan'])
                origin_price = attr_dict['origin_price']
                if not attr_dict.has_key('discount'):
                    discount = get_discount(current_price, origin_price)
                else:
                    discount = attr_dict['discount']
                log.msg("discount = " + str(discount), level=log.DEBUG)

                prod = TaobaoJhsItem()
                prod['link'] = attr_dict['url']
                prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
                prod['title'] = attr_dict['title']
                prod['img'] = img_url
                prod['ori_price'] = origin_price
                prod['cur_price'] = current_price
                prod['discount'] = discount
                prod['sale'] = attr_dict['sale']
                prod['sale_percent'] = sale_percent
                prod['display_time_begin'] = start_time
                prod['display_time_end'] = utils.get_default_end_time()
                if not attr_dict.has_key('li_classname'):
                    prod['stat'] = utils.BEGIN
                elif attr_dict['li_classname'] == 'notbegin':
                    prod['stat'] = utils.NOT_BEGIN
                elif attr_dict['li_classname'] == 'soldout soldout-ju-normal':
                    prod['stat'] = utils.END
                    prod['display_time_end'] = int(time.time())
                else:
                    self.log('unknown state', level = log.ERROR)

                prod['limit'] = attr_dict['limit']
                prod['source'] = self.display_name
                prod['origin_category_name'] = origin_category_name
                prod['category_name'] = category_name
                ret_items.append(prod)
                if debug == True:
                    break
        return ret_items    
