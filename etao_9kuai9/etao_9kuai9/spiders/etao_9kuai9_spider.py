#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib
import time
import hashlib
import decimal
import re
import sys
sys.path.append('../comm_lib')
#from utils import get_one, get_one_string, get_attr, get_obj_attr, get_num, to_fen, get_pic_url, get_item_id, get_discount, UNKNOWN_NUM, UNLIMITED_NUM
import time
import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import socket
import traceback
from etao_9kuai9.items import Etao9Kuai9Item

def get_item_id(url):
    L=re.findall(r'(?<=detail.etao.com/)\w+',url)
    if len(L) > 0:
        return int(L[0])
    return None


class Etao9Kuai9Spider(BaseSpider):
    name = "etao_9kuai9"
    allowed_domains = ["etao.com"]
    start_urls = [
    "http://www.etao.com/"
    ]
    display_name = u'一淘'

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        socket.setdefaulttimeout(60)
        self.cg = utils.CategoryGet(['../tools/1', '../tools/2'])

    def parse(self, response):
        #file = open("a.html", 'w')
        #file.write(response._body)
        #file.close()
        if not utils.get_url_by_browser(self.driver, response.url):
            return
        #xpath='//body/div[@id="container"]/div[@class="page_nm"]/div[@class="mod mod_sp"]/div[@class="mod_sp_inner"]/div[@class="bd"]/ul[@id="red_pro_list"]/li'
        if not utils.click_url(self.driver, '//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@class="content-category"]/ul[@class="cc-items clear-fix"]/li/a[@id="J_Mailfree"]'):
            return

        a_objs = utils.find_elements_by_xpath(self.driver, '//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@id="J_MailContent"]/div[@id="J_MailPanel"]/div/ul[@class="content-items clear-fix mail-category J_MailTmpl"]/li[@class="list-item J_MailItem"]/a')
        a_objs.extend(utils.find_elements_by_xpath(self.driver, '//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@id="J_MailContent"]/div[@id="J_MailPanel"]/div/ul[@class="content-items clear-fix mail-category J_MailTmpl"]/li[@class="list-item J_MailItem list-last-item"]/a'))
        print "len of a_objs " + str(len(a_objs))
        ret_items = []
        for a_obj in a_objs:
            if not utils.click_a_obj(self.driver, a_obj):
                continue
            #while True:
            if not utils.execute_script(self.driver, "window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + 
                    "document.body.scrollHeight,document.documentElement.clientHeight));"):
                continue
            time.sleep(1)
            if not utils.execute_script(self.driver, "window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + 
                    "document.body.scrollHeight,document.documentElement.clientHeight));"):
                continue
            time.sleep(1)
              
            #self.driver.save_screenshot('a.jpg')

            #xpath='//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@id="J_MailContent"]/div[@id="J_MailPanel"]/div/ul/li[@class="cp-item J_Item "]'
            xpath='//li[@class="cp-item J_Item "]'
            li_obj_array = self.driver.find_elements_by_xpath(xpath)
            li_obj_array.extend(self.driver.find_elements_by_xpath('//li[@class="cp-item J_Item cp-item-last"]'))
            print 'len ' + str(len(li_obj_array))
            for li_obj in li_obj_array:
                xpath_list = [
                    ["sale", 'div[@class="item-spec"]', 'text()', 'get_num', None],
                    ["title", 'h3[@class="item-title"]/a', 'text()', 'string', None],
                    ["url", 'h3[@class="item-title"]/a', 'href', 'string', None],
                    ["current_price", 'div[@class="now-price clearfix"]/span[@class="final-price"]/em', 'text()', 'get_float_str_to_fen', None],
                    ['discount_str', 'div[@class="now-price clearfix"]/span[@class="discount"]', 'text()', 'string', None]
                ]
                attr_dict = utils.get_obj_attr(xpath_list, li_obj)
                if not attr_dict:
                    continue

                item_id = get_item_id(attr_dict['url'])
                log.msg('item_id ' + str(item_id), level = log.DEBUG)
                pic_url, url, baoyou, cid = utils.get_taobao_item_info(item_id)
                if not pic_url or not url:
                    log.msg('skip item with no url or pic', level = log.DEBUG)
                    continue

                if not baoyou:
                    log.msg('skip goods because not baoyou', level = log.DEBUG)
                    continue
                origin_category_name, category_name = self.cg.get_cid_name(cid)
                log.msg('origin_category_name ' + origin_category_name + ' category_name ' + category_name + ' title ' + attr_dict['title'] + ' url ' + url, level = log.DEBUG)
                log.msg('pic_url ' + pic_url, level = log.DEBUG)
                log.msg('url ' + url, level = log.DEBUG)
                if attr_dict.has_key('discount_str') and attr_dict['discount_str'] != '':
                    discount = utils.get_discount_int_from_float_str(attr_dict['discount_str'])
                    origin_price = attr_dict['current_price']  * 100 / discount
                else:
                    discount = utils.UNKNOWN_NUM
                    origin_price = utils.UNKNOWN_NUM
                prod = Etao9Kuai9Item()
                log.msg('origin_price ' + str(origin_price), level = log.DEBUG)
                log.msg('discount ' + str(discount), level = log.DEBUG)


                prod['link'] = url 
                prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
                prod['title'] = attr_dict['title']
                prod['img'] = pic_url
                prod['ori_price'] = origin_price
                prod['cur_price'] = attr_dict['current_price']
                if prod['cur_price'] <= 900:
                    log.msg('skip too low price ' + str(prod['cur_price']), level = log.DEBUG)
                    continue
                prod['discount'] = discount
                prod['stat'] = utils.BEGIN
                prod['sale'] = utils.UNKNOWN_NUM
                prod['sale_percent'] = utils.UNKNOWN_NUM
                prod['display_time_begin'] = utils.get_default_start_time()
                prod['display_time_end'] = utils.get_default_end_time()
                #prod['actual_time_begin'] = start_time
                #prod['actual_time_end'] = start_time
                prod['limit'] = utils.UNLIMITED_NUM
                prod['source'] = self.display_name
                prod['origin_category_name'] = origin_category_name
                prod['category_name'] = category_name
                ret_items.append(prod)

                #next_page_xpath = '//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@id="J_MailContent"]/div[@id="J_MailPanel"]/div/div[@class="J_Paging pagination"]/div[@class="pagination-pages"]/div[@class="pagination-pages"]/div[@class="pagination-page"]/a[@class="page-next"]'
                #if not utils.click_url(self.driver, next_page_xpath):
                #    print 'no next page'
                #    break
        print 'ret_items ' + str(len(ret_items))
        return ret_items
