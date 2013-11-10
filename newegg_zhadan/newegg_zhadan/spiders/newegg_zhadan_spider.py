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
import utils

class NewegZhadanSpider(BaseSpider):
    name = "newegg_zhadan"
    allowed_domains = ["newegg.com.cn"]
    start_urls = [
            "http://zhadan.newegg.com.cn/"
    ]

    def parse_page(self, url):
        buffer = utils.get_url_content(url)
        if not buffer:
            return False
        hxs = HtmlXPathSelector(text=buffer)
        h_div = utils.get_one(hxs.select('//body/div[@id="wrap"]/div[@class="wraper"]/div[@id="body"]/div[@id="body"]/div/div[@id="proCtner"]'))
        xpath_list = [
            ["pic_url", 'div[@id="proMainInfo"]/div[@class="mainLeft"]/div[@class="bigImgArea"]/dl/dt[@class="mainShow"]/a[@id="bigImg"]/@href', 'string', None],
            #['']
        ]
        attr_dict = utils.get_attr(xpath_list, h_div)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        h_li_array = hxs.select('//body/div[@id="wrap"]/div[@class="wraper"]/div[@id="body"]/div[@id="body"]/div[@class="sliderA"]/div[@class="inner"]/ul/li')
        print "len " + str(len(h_li_array))
        for h_li in h_li_array:
            xpath_list = [
                ["url", 'a/@href', 'string', None],
            ]
            attr_dict = utils.get_attr(xpath_list, h_li)
            self.parse_page(attr_dict['url'])
            break

        next_page = utils.get_one(hxs.select('//body/div[@id="wrap"]/div[@class="wraper"]/div[@id="body"]/div[@id="body"]/div[@class="sliderA"]/div[@class="inner"]/a/@href').extract())
        file = open("a.html", 'w')
        file.write(response._body)
        file.close()
        if next_page:
            print 'next_page ' + next_page
