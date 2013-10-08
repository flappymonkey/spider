#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib
from gome_groupon.items import GomeGrouponItem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def get_one(array):
    if len(array) > 0:
        return array[0]
    else:
        return None
def get_one_string(array):
    if len(array) > 0:
        return array[0]
    else:
        return ""
#['title', 'p[@class="name"]/a/@title', 'get_one'],
def get_attr(xpath_list, h):
    attr_dict = {}
    for attr_info in xpath_list:
        attr_name = attr_info[0]
        xpath = attr_info[1]
        func = attr_info[2]
        if func == 'get_one':
            attr_value = get_one(h.select(xpath).extract())
        else:
            attr_value = get_one_string(h.select(xpath).extract())
        if not attr_value:
            print attr_name + " None"
        else:
            attr_dict[attr_name] = attr_value
            print attr_name + " " + attr_dict[attr_name].encode('utf8')
    return attr_dict

#['title', 'p[@class="name"]/a', 'title', 'get_one'],
def get_obj_attr(xpath_list, obj):
    attr_dict = {}
    for attr_info in xpath_list:
        attr_name = attr_info[0]
        xpath = attr_info[1]
        tag_attr = attr_info[2]
        func = attr_info[3]
        try:
            if tag_attr == 'text()':
                attr_value = obj.find_element_by_xpath(xpath).text
            else:
                attr_value = obj.find_element_by_xpath(xpath).get_attribute(tag_attr)
        except NoSuchElementException:
            print attr_name + " None"
            if func == "get_one":
                attr_value = None
            else:
                attr_value = ""
                attr_dict[attr_name] = attr_value
        else:
            attr_dict[attr_name] = attr_value
            print attr_name + " " + attr_dict[attr_name].encode('utf8')
    return attr_dict

class GomeGrouponSpider(BaseSpider):
    name = "gome_groupon"
    allowed_domains = ["g.gome.com.cn"]
    start_urls = [
    "http://g.gome.com.cn/ec/groupon/groupon/todayGroupOn.jsp"
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)

    def parse(self, response):
        '''
        hxs = HtmlXPathSelector(response)
        h_li_array = hxs.select('//body/div[@class="tuan-main clearfix"]/ul[@class="tuan-list"]/li')
        xpath_list = [
            ['title', 'p[@class="name"]/a/@title', 'get_one'],
            ['url', 'p[@class="name"]/a/@href', 'get_one'],
            ['img_url', 'p[@class="pic"]/a/@href', 'get_one'],
            ['sale', 'p[@class="buy-state clearfix"]/span[@class="orig-buyed"]/strong/text()', 'get_one'],
            ['origin_price_yuan_str', 'p[@class="actions clearfix"]/span[@class="price"]/text()', 'get_one'],
            ['origin_price_fen_str', 'p[@class="actions clearfix"]/span[@class="price"]/em[@class="zero"]/text()', 'get_string']
        ]
        for h_li in h_li_array:
            prod = GomeGrouponItem()
            attr_dict = get_attr(xpath_list, h_li)
        file = open("a.html", 'w')
        file.write(response._body)
        file.close()
        '''
        if not utils.get_url_by_browser(self.driver, response.url):
            return
        li_obj_array = self.driver.find_elements_by_xpath('//body/div[@class="tuan-main clearfix"]/ul[@class="tuan-list"]/li')
        xpath_list = [
            ['title', 'p[@class="name"]/a', 'title', 'get_one'],
            ['url', 'p[@class="name"]/a', 'href', 'get_one'],
            ['img_url', 'p[@class="pic"]/a', 'href', 'get_one'],
            ['sale', 'p[@class="buy-state clearfix"]/span[@class="orig-buyed"]/strong', 'text()', 'get_one'],
            ['current_price_yuan_str', 'p[@class="actions clearfix"]/span[@class="price"]', 'text()', 'get_one'],
            ['current_price_fen_str', 'p[@class="actions clearfix"]/span[@class="price"]/em[@class="zero"]', 'text()', 'get_string']
        ]
        for li_obj in li_obj_array:
            get_obj_attr(xpath_list, li_obj)
