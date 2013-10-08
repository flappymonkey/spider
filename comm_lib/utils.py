#coding=utf-8
import decimal
import re
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import urllib
import urllib2
import time
import hashlib 
import md5 
import ast
from scrapy import log
import traceback
from datetime import datetime

UNKNOWN_NUM = -1
UNLIMITED_NUM = 0
NOT_BEGIN = 1
BEGIN = 2
END = 3
class OpenTaobao:
    def __init__(self,app_key,sercet_code):
        self.app_key = app_key
        self.sercet_code = sercet_code
    def get_time(self):
        t = time.localtime()
        return time.strftime('%Y-%m-%d %X', t)
    def get_sign(self,params):
        params['format'] = 'json' 
        params.update({'app_key':self.app_key,'timestamp':self.get_time(),'v':'2.0'})
        src = self.sercet_code + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())])
        return md5.new(src).hexdigest().upper()
    def get_result(self,params):
        params['sign'] = self.get_sign(params)
        form_data = urllib.urlencode(params)
        return urllib2.urlopen('http://gw.api.taobao.com/router/rest', form_data).read()
    
def get_pic_url(num_iid):
    try:
        op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
        params = {
            'method':'taobao.item.get',
            'fields':'pic_url',
            'num_iid':str(num_iid),
        }
        dict_str = op.get_result(params)
        ret_dict = ast.literal_eval(dict_str)
        if ret_dict.has_key('item_get_response'):
            if ret_dict['item_get_response'].has_key('item'):
                if ret_dict['item_get_response']['item'].has_key('pic_url'):
                    return ret_dict['item_get_response']["item"]["pic_url"].replace('\/', '/')
        return None
    except:
        exstr = traceback.format_exc()
        log.msg('failed to get_pic_url ' + exstr, level = log.WARNING)
        return None

def get_left_goods(num_iid):
    try:
        op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
        params = {
            'method':'taobao.item.get',
            'fields':'num',
            'num_iid':str(num_iid),
        }
        dict_str = op.get_result(params)
        ret_dict = ast.literal_eval(dict_str)
        if ret_dict.has_key('item_get_response'):
            if ret_dict['item_get_response'].has_key('item'):
                if ret_dict['item_get_response']['item'].has_key('num'):
                    return int(ret_dict['item_get_response']["item"]["num"])
    except:
        exstr = traceback.format_exc()
        log.msg('failed to get_pic_url ' + exstr, level = log.WARNING)
        return None

def get_item_id(url):
    L=re.findall(r'(?<=item_id=)\w+',url)
    if len(L) > 0:
        return int(L[0])
    return None

def get_id(url):
    L=re.findall(r'(?<=id=)\w+',url)
    if len(L) > 0:
        return int(L[0])
    return None

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

def get_num(string):
    list_str = re.findall('[0-9]*', string)
    for elem in list_str:
        if elem != "":
            return int(elem)
    return None

def get_float_str(string):
    list_str = re.findall('[0-9\.]*', string)
    for elem in list_str:
        if elem != "":
            return elem
    return None

def to_fen(price_str):
    return int(float(price_str) * 100)

def get_float_str_to_fen(string):
    price_str = get_float_str(string)
    if not price_str:
        return None
    return to_fen(get_float_str(string))

def get_discount(current_price, origin_price):
    discount = float(current_price * 100)/float(origin_price)
    return int (round(discount, 0))
#    return int((current_price/origin_price) * 100)
#2.8折 => 28
def get_discount_int(discount_str):
    return int(float(discount_str) * 10)

def set_origin_value(item, cursor, key):
    if cursor.has_key(key):
        origin_value = cursor[key]
        item[key] = origin_value

def set_origin_value_if_db_smaller(item, cursor, key):
    if cursor and cursor.has_key(key) and item.has_key(key):
        if cursor[key] < item[key]:
            origin_value = cursor[key]
            item[key] = origin_value
            return True
    return False

def status_to_str(stat):
    if stat == NOT_BEGIN:
        return 'not_begin'
    elif stat == BEGIN:
        return 'begin'
    elif stat == END:
        return 'end'
    else:
        return 'unknown status'

def check_status(item, cursor):
    if not cursor:
        log.msg('first status [%s] url [%s]'% (status_to_str(item['stat']), item['link']), level = log.DEBUG)
    if cursor and cursor.has_key('stat') and item.has_key('stat'):
        if cursor['stat'] != item['stat']:
            log.msg('change status [%s] -> [%s] url [%s]'% (status_to_str(cursor['stat']), status_to_str(item['stat']), item['link']), level = log.DEBUG)

def set_origin_value_list(item, cursor, key_list):
    if cursor :
        for key in key_list:
            if cursor.has_key(key):
                origin_value = cursor[key]
                item[key] = origin_value

def get_url_by_browser(driver, url):
    try:
        driver.get(url)
        return True
    except TimeoutException:
        exstr = traceback.format_exc()
        log.msg('exception timeout when driver.get url ' + url + " " + str(exstr), level = log.WARNING)
        return False
    except:
        exstr = traceback.format_exc()
        log.msg('failed when driver.get url ' + url + " " + str(exstr), level = log.WARNING)
        return False

def get_current_url(driver):
    try:
        return driver.current_url
    except:
        exstr = traceback.format_exc()
        log.msg('failed when return driver.current_url ' + str(exstr), level = log.WARNING)
        return None

#['title', 'div[@class="product-summary"]/div[@class="product-main-title"]/h1[@class="wb"]/@title', 'string', None],
def get_attr(xpath_list, h):
    attr_dict = {}
    for attr_info in xpath_list:
        attr_name = attr_info[0]
        xpath = attr_info[1]
        func = attr_info[2]
        default_value = attr_info[3]
        attr_value = get_one(h.select(xpath).extract())
        if not attr_value:
            attr_value = default_value
            log.msg(attr_name + " None", level = log.DEBUG)
            if attr_value != None:
                attr_dict[attr_name] = attr_value
        else:
            log.msg(attr_name + " [" + attr_value.encode('utf8') + ']', level = log.DEBUG)
            if func == 'int':
                attr_dict[attr_name] = int(attr_value)
            elif func == 'float':
                attr_dict[attr_name] = float(attr_value)
            elif func == 'string':
                attr_dict[attr_name] = attr_value
            elif func == 'strip':
                attr_dict[attr_name] = attr_value.strip()
            elif func == 'to_fen':
                attr_dict[attr_name] = to_fen(attr_value)
            elif func == 'get_num':
                attr_dict[attr_name] = get_num(attr_value)
            elif func == 'get_discount_int':
                attr_dict[attr_name] = get_discount_int(attr_value)
            elif func == 'get_float_str_to_fen':
                attr_dict[attr_name] = get_float_str_to_fen(attr_value)
            else:
                log.msg("error unknown func " + func, level = log.ERROR)
                return None
            if func != 'string' and func != 'strip':
                log.msg(attr_name + " [" + str(attr_dict[attr_name]) + ']', level = log.DEBUG)
            else:
                log.msg(attr_name + " [" + attr_dict[attr_name].encode('utf8') + ']', level = log.DEBUG)
    return attr_dict

#['title', 'div[@class="product-summary"]/div[@class="product-main-title"]/h1[@class="wb"]', 'title', 'string', None],
def get_obj_attr(xpath_list, obj):
    attr_dict = {}
    for attr_info in xpath_list:
        attr_name = attr_info[0]
        xpath = attr_info[1]
        tag_attr = attr_info[2]
        func = attr_info[3]
        default_value = attr_info[4]
        try:
            if tag_attr == 'text()':
                attr_value = obj.find_element_by_xpath(xpath).text
            else:
                attr_value = obj.find_element_by_xpath(xpath).get_attribute(tag_attr)
        except NoSuchElementException:
            log.msg(attr_name + " None", level = log.DEBUG)
            attr_value = default_value
            if attr_value != None:
                attr_dict[attr_name] = attr_value
        else:
            log.msg(attr_name + " [" + attr_value.encode('utf8') + ']', level = log.DEBUG)
            if func == 'int':
                attr_dict[attr_name] = int(attr_value)
            elif func == 'float':
                attr_dict[attr_name] = float(attr_value)
            elif func == 'string':
                attr_dict[attr_name] = attr_value
            elif func == 'strip':
                attr_dict[attr_name] = attr_value.strip()
            elif func == 'to_fen':
                attr_dict[attr_name] = to_fen(attr_value)
            elif func == 'get_num':
                attr_dict[attr_name] = get_num(attr_value)
            elif func == 'get_discount_int':
                attr_dict[attr_name] = get_discount_int(attr_value)
            elif func == 'get_float_str_to_fen':
                attr_dict[attr_name] = get_float_str_to_fen(attr_value)
            else:
                log.msg("error unknown func " + func, level = log.ERROR)
                return None
            if func != 'string':
                log.msg(attr_name + " [" + str(attr_dict[attr_name]) + ']', level = log.DEBUG)
            else:
                log.msg(attr_name + " [" + attr_dict[attr_name].encode('utf8') + ']', level = log.DEBUG)
    return attr_dict

def get_default_end_time():
    end_time_str = str(datetime.now().date()) + " 23:59:59"
    end_time = int(datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
    return end_time

def get_default_start_time():
    start_time_str = str(datetime.now().date()) + " 00:00:00"
    start_time = int(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
    return start_time

def find_element_by_xpath(driver, xpath):
    try:
        a_obj = driver.find_element_by_xpath(xpath)
        return a_obj
    except NoSuchElementException:
        exstr = traceback.format_exc()
        log.msg('failed to find_element_by_xpath ' + xpath, level = log.ERROR)
        return None
