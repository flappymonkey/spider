#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.http import FormRequest
import json as simplejson
import httplib, urllib

class TemplateSpider(BaseSpider):
    name = "template"
    allowed_domains = ["yixun.com"]
    start_urls = [
    "http://sale.yixun.com/nightmarket.html?YTAG=1.100000804"
    ]

    def parse(self, response):
        file = open("a.html", 'w')
        file.write(response._body)
        file.close()
