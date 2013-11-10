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
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
sys.path.append('../comm_lib')
from etao_smzdm.items import EtaoSmzdmItem
import time
import datetime
import utils
import socket
import hashlib

class EtaoSmzdmSpider(BaseSpider):
    name = "etao_smzdm"
    allowed_domains = ["etao.com"]
    start_urls = [
            "http://www.etao.com/"
    ]
    total_pages = 50
    display_name = u'一淘'
    
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        socket.setdefaulttimeout(60)
        self.record_num = 0

    def parse(self, response):
        if not utils.get_url_by_browser(self.driver, response.url):
            return
        time.sleep(2)
        for i in xrange(2):
            if not utils.execute_script(self.driver, "window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + 
                    "document.body.scrollHeight,document.documentElement.clientHeight));"):
                return
            time.sleep(1)
        div_obj_array = utils.find_elements_by_xpath(self.driver, '//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@id="J_FeedContent"]/div[@id="J_FeedPanel"]/div[@bx-name="feedlist"]/div[@id="J_FeedList"]/div[@class="feed-page"]/div[@class="feed   "]', log.DEBUG)
        i = 0
        #print len(div_obj_array)
        prod_list = []
        for div_obj in div_obj_array:
            xpath_list = [
                ['title', 'div[@class="module feed11 clearfix"]/div[@class="feed-hd"]/h3[@class="feed-title"]/a', 'title', 'string', None],
                ['title_red', 'div[@class="module feed11 clearfix"]/div[@class="feed-hd"]/h3[@class="feed-title"]/a/strong', 'text()', 'string', None],
                ['link', 'div[@class="module feed11 clearfix"]/div[@class="feed-hd"]/h3[@class="feed-title"]/a', 'href', 'string', None],
                ['img_url', 'div[@class="module feed11 clearfix"]/div[@class="feed-img feed-img-180"]/a/img', 'src', 'string', None],
                ['description', 'div[@class="module feed11 clearfix"]/div[@class="feed-bd clearfix"]/div[@class="feed-desc"]/p', 'text()', 'string', None],
                ['pub_time', 'div[@class="feed-data clearfix"]/div[@class="feed-info"]/span[@class="feed-pub-time"]', 'text()', 'string', None, 1],
            ]
            attr_dict = utils.get_obj_attr(xpath_list, div_obj)
            if not attr_dict.has_key('title'):
                continue
            self.record_num = self.record_num + 1
            prod = EtaoSmzdmItem()
            prod['id'] = hashlib.md5(attr_dict['link']).hexdigest().upper()
            prod['title'] = [attr_dict['title']]
            if prod.has_key('title_red'):
                prod['title'].append(attr_dict['title_red'])
            prod['img'] = [attr_dict['img_url']]
            prod['source_url'] = attr_dict['link']
            prod['desc'] = [attr_dict['description']]
            prod['pub_time'] = str(datetime.date.today().year) + '-' + attr_dict['pub_time'] + ':00'
            prod['stat'] = 0
            prod['crawl_source'] = self.display_name
            prod['source'] = self.display_name
            prod['link_desc'] = ""
            prod['desc_link_list'] = []
            prod['go_link'] = []
            prod['cat'] = []
            prod['worth_num'] = 0
            prod['bad_num'] = 0
            prod['flag'] = 0
            prod['need_filter'] = 1
            prod['same_id'] = "NONE"
            if self.record_num > self.total_pages:
                break
            prod_list.append(prod)
        print 'prod_list ' + str(len(prod_list))
        if self.record_num < self.total_pages:
            next_page_obj = utils.find_element_by_xpath(self.driver, '//body/div[@class="etao-content clearfix"]/div[@class="main-content"]/div[@id="J_SwitchContent"]/div[@id="J_FeedContent"]/div[@id="J_FeedPanel"]/div[@bx-name="feedlist"]/div[@class="J_Paging pagination"]/div[@id="J_FeedsPage"]/div[@class="pagination-pages"]/div[@class="pagination-page"]', log.DEBUG)
            xpath_list=[ ['next_page', 'a[@class="page-next"]', 'href', 'string', None]]
            attr_dict = utils.get_obj_attr(xpath_list, next_page_obj)
            if not attr_dict or not attr_dict.has_key('next_page'):
                return
            next_page =  attr_dict['next_page']
            prod_list.append(Request(url=next_page, callback=self.parse))
        return prod_list
