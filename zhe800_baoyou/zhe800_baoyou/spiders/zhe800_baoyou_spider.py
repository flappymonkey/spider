#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib
from zhe800_baoyou.items import Zhe800BaoyouItem
import hashlib
from datetime import datetime, date, time, timedelta
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import decimal
import re
import sys
sys.path.append('../comm_lib')
from utils import get_one, get_one_string, get_attr, get_obj_attr, get_num, to_fen, get_discount, get_pic_url, get_item_id, get_discount, UNKNOWN_NUM, UNLIMITED_NUM, get_float_str_to_fen
import time
import utils
import code, traceback, signal
import socket

def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
        interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)
    i = code.InteractiveConsole(d)
    message  = "Signal recieved : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)
    exstr = traceback.format_exc()
    print exstr

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler

listen()

def get_datetime(string):
    list1 = re.findall('[0-9]*', string)
    list2 = []
    for elem in list1:
        if elem != "":
            list2.append(elem)
    start_time_str = str(date.today().year) + "-" + list2[0] + "-" + list2[1] + " " + list2[2] + ":" + list2[3] + ":00"
    start_time = int(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))    
    return start_time

def get_url():
    try:
        a_obj = self.driver.find_element_by_xpath('//body/div[@id="dialog_out_weldeal"]/div[@class="diginfo"]/div[@class="weloutdialog"]/div[@id="ppLogin"]/form[@name="loginform"]/ul/li[@class="reg"]/a')
        a_obj.click()
        time.sleep(2)

        url = self.driver.current_url
    except:
        return None
    return url

debug = False

class Zhe800BaoyouSpider(BaseSpider):
    name = "zhe800_baoyou"
    allowed_domains = ["www.zhe800.com"]
    start_urls = [
    "http://www.zhe800.com/ju_type/baoyou"
    ]
    display_name = u'淘宝'

    def recreate_driver(self):
        self.driver.quit()
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        socket.setdefaulttimeout(20)

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        socket.setdefaulttimeout(20)

    def get_next_page(self, response):
        hxs = HtmlXPathSelector(response)
        h_a_array = hxs.select('//body/div[@class="page_div clear area page_bottom"]/div[@class="list_page"]/span[@class="next"]/a/@href')
        if len(h_a_array) > 0:
            log.msg("next url " + h_a_array[0].extract(), level = log.DEBUG)
            return h_a_array[0].extract()
        return None

    #def login(self):
    #    self.driver.

    def parse(self, response):
        '''
        file = open("a.html", 'w')
        file.write(response._body)
        file.close()
        return
        '''
        ret_items = []
        next_url = self.get_next_page(response)
        if next_url:
            ret_items.append(Request(url=next_url,dont_filter=True,callback=self.parse))
        log.msg('url ' + response._url, level = log.DEBUG)
        #return ret_items 
        hxs = HtmlXPathSelector(response)
        h_div_array = hxs.select('//body/div[@class="area"]/div[@class="dealbox"]/div')
        i = 0
        for h_div in h_div_array:
            xpath_list = [
                ['login_url', 'div/p/a/@href', 'string', None],
                ['img_url', 'div/p/a/img/@src', 'string', None],
                ['origin_img_url', 'div/p/a/img/@data-original', 'string', None],
                ['title', 'div/h2/a/text()', 'string', None],
                ['current_price_yuan_str', 'div/h4/span/em/text()', 'string', None],
                ['current_price_fen_str', 'div/h4/span/em/em/text()', 'string', ""],
                ['origin_price', 'div/h4/span/i/text()', 'get_float_str_to_fen', None],
                ['start_time_str', 'div/h5/span/text()', 'string', None],
            ]
            attr_dict = get_attr(xpath_list, h_div)
            start_time = get_datetime(attr_dict['start_time_str'])
            if start_time < utils.get_default_start_time():
                log.msg('skip too old time ', level = log.DEBUG)
                continue

            current_price = get_float_str_to_fen(attr_dict['current_price_yuan_str'] + attr_dict['current_price_fen_str'])
            i = i + 1
            log.msg('opentab count ' + str(i), level = log.DEBUG)
            if i % 5 == 0:
                self.recreate_driver()
                log.msg('recreate_driver i ' + str(i), level = log.DEBUG)
            if not utils.get_url_by_browser(self.driver, attr_dict['login_url']):
                continue
            log.msg('after get_url_by_browser ', level = log.DEBUG)
            #a_obj = self.driver.find_element_by_xpath('//body/div[@id="dialog_out_weldeal"]/div[@class="diginfo"]/div[@class="weloutdialog"]/div[@id="ppLogin"]/form[@name="loginform"]/ul/li[@class="reg"]/a')
            a_obj = utils.find_element_by_xpath(self.driver, '//body/div[@id="dialog_out_weldeal"]/div[@class="diginfo"]/div[@class="weloutdialog"]/div[@id="ppLogin"]/form[@name="loginform"]/ul/li[@class="reg"]/a')
            log.msg('after find_element_by_xpath ', level = log.DEBUG)
            if not a_obj:
                log.msg('Faild to get url from login_url ' + attr_dict['login_url'], level = log.ERROR)
                continue
            a_obj.click()
            log.msg('after click ', level = log.DEBUG)
            #time.sleep(2)

            #url = self.driver.current_url
            origin_url = utils.get_current_url(self.driver)
            if not origin_url:
                continue
            if origin_url.find('http://s.click.taobao.com') != -1 :
                log.msg('skip invalid url ' + origin_url, level = log.DEBUG)
                continue
            url = origin_url.split('&')[0]
            #url = 'http://www.example.com'
            log.msg('after current_url ' + url, level = log.DEBUG)

            discount = get_discount(current_price, attr_dict['origin_price'])
            self.log("discount " + str(discount), level = log.DEBUG)

            if attr_dict.has_key('origin_img_url') and attr_dict['origin_img_url'][-4:] == '.jpg':
                img_url = attr_dict['origin_img_url']
            elif attr_dict.has_key('img_url') and attr_dict['img_url'][-4:] == '.jpg':
                img_url = attr_dict['img_url']
            else:
                log.msg('skip invalid img_url ' + attr_dict['img_url'], level = log.WARNING)
                continue

            prod = Zhe800BaoyouItem()
            prod['link'] = url
            prod['id'] = hashlib.md5(prod['link']).hexdigest().upper()
            prod['title'] = attr_dict['title']
            prod['img'] = img_url
            prod['ori_price'] = attr_dict['origin_price']
            prod['cur_price'] = current_price
            prod['discount'] = discount
            prod['stat'] = utils.BEGIN
            prod['sale'] = UNKNOWN_NUM
            prod['sale_percent'] = UNKNOWN_NUM
            prod['display_time_begin'] = start_time
            prod['display_time_end'] = utils.get_default_end_time()
            #prod['display_time_end'] = start_time
            #prod['actual_time_begin'] = start_time
            #prod['actual_time_end'] = start_time
            prod['limit'] = UNLIMITED_NUM
            prod['source'] = self.display_name
            ret_items.append(prod)
            if debug :
                break
        return ret_items

