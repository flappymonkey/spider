#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import unittest
sys.path.append('../comm_lib')
sys.path.append('../taobao_jhs/taobao_jhs/spiders')
sys.path.append('../taobao_jhs/taobao_jhs')
sys.path.append('../taobao_jhs')
import taobao_jhs_spider
from scrapy import log
from scrapy.http import Response, Request
from scrapy.http.response.html import HtmlResponse
from taobao_jhs.items import TaobaoJhsItem
import utils
import datetime

def fake_response_from_file(file_name, url = None):
    if not url:
        url = 'http://www.example.com'
    file_content = open(file_name, 'r').read()
    request = Request(url=url)
    response = HtmlResponse(url=url, request=request, body=file_content)
#    response.encoding = 'utf-8'
    return response

def print_type(elem, str_before=""):
    elem_type = elem.__class__.__name__
    str_before = str_before + elem_type + "  "
    if elem_type == 'list':
        for e in elem:
            print_type(e, str_before)
    elif elem_type == 'Request':
        print str_before + elem._url
    else:
        print str_before + elem_type

def parse_result(elem, class_dict):
    elem_type = elem.__class__.__name__
    if elem_type == 'list':
        for e in elem:
            parse_result(e, class_dict)
    else:
        if not class_dict.has_key(elem_type):
            class_dict[elem_type] = []
        class_dict[elem_type].append(elem)

class TaobaoJhsSpiderTestCase(unittest.TestCase):
    def setUp(self):
        self.spider = taobao_jhs_spider.TaobaoJhsSpider()
    def testParse(self):
        results = self.spider.parse(fake_response_from_file('html/taobao_jhs.html'))
        #results = self.spider.parse(fake_response_from_file('html/a.html'))
#        print_type(results)
        class_dict = {}
        parse_result(results, class_dict)

        date_str = str(datetime.datetime.now().date())
        tomorrow_date_str = str((datetime.datetime.now() + datetime.timedelta(days = 1)).date())
        self.assertEquals(len(class_dict['Request']), 2)
        self.assertEquals(len(class_dict['TaobaoJhsItem']), 29)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['limit'], 100)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['cur_price'], 5980)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['ori_price'], 19980)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['discount'], 30)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['sale'], 100)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['sale_percent'], 100)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['stat'], utils.END)
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['title'], u'[包邮]【整点聚】ASD/爱仕达24cm无油烟  色彩靓丽 高效节能 平底煎锅WG8224E（每个ID限购2件）')
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['display_time_begin'], int(datetime.datetime.strptime(date_str + ' 15:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")))
        self.assertEquals(class_dict['TaobaoJhsItem'][0]['img'], 'http://img02.taobaocdn.com/bao/uploaded/i2/12446028456146654/T1oo12FideXXXXXXXX_!!0-item_pic.jpg')
        #TODO
        #self.assertEquals(class_dict['TaobaoJhsItem'][0]['display_time_end'], int(datetime.datetime.strptime(date_str + ' 18:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")))
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['limit'], utils.UNLIMITED_NUM)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['cur_price'], 980)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['ori_price'], 5000)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['discount'], 19)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['sale'], utils.UNKNOWN_NUM)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['sale_percent'], utils.UNKNOWN_NUM)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['stat'], utils.NOT_BEGIN)
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['title'], u'[16:00开团][包邮]【整点聚】[梅安]荞麦茶 苦荞茶 四川凉山 苦荞麦茶 黑苦荞茶200g（每个ID限购10件）')
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['display_time_begin'], int(datetime.datetime.strptime(date_str + ' 16:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")))
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['display_time_end'], int(datetime.datetime.strptime(tomorrow_date_str + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")))
        self.assertEquals(class_dict['TaobaoJhsItem'][6]['img'], 'http://img01.taobaocdn.com/bao/uploaded/i1/12933028498170710/T14sC4FkpfXXXXXXXX_!!0-item_pic.jpg')
        self.assertEquals(class_dict['Request'][0]._url, 'http://ju.taobao.com/tg/point_list.htm?from=top&page=2#pointnav')
        self.assertEquals(class_dict['Request'][1]._url, 'http://ju.taobao.com/tg/point_list.htm?day=1')
if __name__ == '__main__':
    #log.start(logstdout = True, loglevel = log.DEBUG)
    import doctest, taobao_jhs_spider
    doctest.testmod(taobao_jhs_spider)
    unittest.main()
