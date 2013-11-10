#! /usr/bin/env python
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
import os
import simplejson as json

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

def get_pic_url_and_detail_url(num_iid):
    try:
        op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
        params = {
            'method':'taobao.item.get',
            'fields':'pic_url, detail_url',
            'num_iid':str(num_iid),
        }
        dict_str = op.get_result(params)
        ret_dict = ast.literal_eval(dict_str)
        return ret_dict['item_get_response']["item"]["pic_url"].replace('\/', '/'),  ret_dict['item_get_response']["item"]["detail_url"].replace('\/', '/')
    except:
        exstr = traceback.format_exc()
        log.msg('failed to get_pic_and_detail_url ' + exstr, level = log.WARNING)
        return None, None


def get_taobao_item_info(num_iid):
    try:
        op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
        params = {
            'method':'taobao.item.get',
            'fields':'pic_url, detail_url, post_fee, express_fee, ems_fee, freight_payer, cid',
            'num_iid':str(num_iid),
        }
        dict_str = op.get_result(params)
        ret_dict = ast.literal_eval(dict_str)
        if ret_dict['item_get_response']["item"]["post_fee"] == '0.00' or ret_dict['item_get_response']["item"]["express_fee"] == '0.00' or ret_dict['item_get_response']["item"]["freight_payer"] == 'seller':
            baoyou = True
        else:
            baoyou = False
        log.msg('post_fee ' + str(ret_dict['item_get_response']["item"]["post_fee"]) + ' express_fee ' + str(ret_dict['item_get_response']["item"]["express_fee"]) + ' ems_fee ' + str(ret_dict['item_get_response']["item"]["ems_fee"]) + ' freight_payer ' + str(ret_dict['item_get_response']["item"]["freight_payer"]) + ' baoyou ' + str(baoyou), level = log.DEBUG)
        return ret_dict['item_get_response']["item"]["pic_url"].replace('\/', '/'),  ret_dict['item_get_response']["item"]["detail_url"].replace('\/', '/'), baoyou, ret_dict['item_get_response']["item"]["cid"]
    except:
        exstr = traceback.format_exc()
        log.msg('failed to get_pic_and_detail_url ' + exstr, level = log.WARNING)
        return None, None, None, None

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

def get_task_id(string):
    L=re.findall(r'(?<=TaskId=)\w+', string)
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
    if price_str == '':
        return None
    return to_fen(get_float_str(string))

def get_discount(current_price, origin_price):
    discount = float(current_price * 100)/float(origin_price)
    return int (round(discount, 0))
#    return int((current_price/origin_price) * 100)
#2.8折 => 28
def get_discount_int(discount_str):
    return int(float(discount_str) * 10)

def get_discount_int_from_float_str(string):
    return get_discount_int(get_float_str(string))

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
        try:
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
                    real_attr_value = int(attr_value)
                elif func == 'float':
                    real_attr_value = float(attr_value)
                elif func == 'string':
                    real_attr_value = attr_value
                elif func == 'strip':
                    real_attr_value = attr_value.strip()
                elif func == 'to_fen':
                    real_attr_value = to_fen(attr_value)
                elif func == 'get_num':
                    real_attr_value = get_num(attr_value)
                elif func == 'get_discount_int':
                    real_attr_value = get_discount_int(attr_value)
                elif func == 'get_float_str_to_fen':
                    real_attr_value = get_float_str_to_fen(attr_value)
                elif func == 'get_discount_int_from_float_str':
                    real_attr_value = get_discount_int_from_float_str(attr_value)
                else:
                    log.msg("error unknown func " + func, level = log.ERROR)
                    return None
                if not real_attr_value:
                    real_attr_value = default_value
                if real_attr_value:
                    attr_dict[attr_name] = real_attr_value
                if attr_dict.has_key(attr_name):
                    if func != 'string' and func != 'strip':
                        log.msg(attr_name + " [" + str(attr_dict[attr_name]) + ']', level = log.DEBUG)
                    else:
                        log.msg(attr_name + " [" + attr_dict[attr_name].encode('utf8') + ']', level = log.DEBUG)
                else:
                    log.msg(attr_name + " None", level = log.DEBUG)
        except:
            exstr = traceback.format_exc()
            log.msg('failed to get attr_name [' + attr_name + '] attr_value [' + attr_value + '] ' + exstr, level = log.ERROR)
            return None
    return attr_dict

#['title', 'div[@class="product-summary"]/div[@class="product-main-title"]/h1[@class="wb"]', 'title', 'string', None],
def get_obj_attr(xpath_list, obj):
    attr_dict = {}
    for attr_info in xpath_list:
        try:
            attr_name = attr_info[0]
            xpath = attr_info[1]
            tag_attr = attr_info[2]
            func = attr_info[3]
            default_value = attr_info[4]
            index = 0
            if len(attr_info) > 5:
                index = attr_info[5]
            try:
                if tag_attr == 'text()':
                    if index == 0:
                        attr_value = obj.find_element_by_xpath(xpath).text
                    else:
                        attr_value = obj.find_elements_by_xpath(xpath)[index].text
                else:
                    if index == 0:
                        attr_value = obj.find_element_by_xpath(xpath).get_attribute(tag_attr)
                    else:
                        attr_value = obj.find_elements_by_xpath(xpath)[index].get_attribute(tag_attr)
            except NoSuchElementException:
                log.msg(attr_name + " None", level = log.DEBUG)
                attr_value = default_value
                if attr_value != None:
                    attr_dict[attr_name] = attr_value
            else:
                log.msg(attr_name + " [" + attr_value.encode('utf8') + ']', level = log.DEBUG)
                if func == 'int':
                    real_attr_value = int(attr_value)
                elif func == 'float':
                    real_attr_value = float(attr_value)
                elif func == 'string':
                    real_attr_value = attr_value
                elif func == 'strip':
                    real_attr_value = attr_value.strip()
                elif func == 'to_fen':
                    real_attr_value = to_fen(attr_value)
                elif func == 'get_num':
                    real_attr_value = get_num(attr_value)
                elif func == 'get_discount_int':
                    real_attr_value = get_discount_int(attr_value)
                elif func == 'get_float_str_to_fen':
                    real_attr_value = get_float_str_to_fen(attr_value)
                elif func == 'get_discount_int_from_float_str':
                    real_attr_value = get_discount_int_from_float_str(attr_value)
                else:
                    log.msg("error unknown func " + func, level = log.ERROR)
                    return None
                if not real_attr_value:
                    real_attr_value = default_value
                if real_attr_value:
                    attr_dict[attr_name] = real_attr_value
                if attr_dict.has_key(attr_name):
                    if func != 'string':
                        log.msg(attr_name + " [" + str(attr_dict[attr_name]) + ']', level = log.DEBUG)
                    else:
                        log.msg(attr_name + " [" + attr_dict[attr_name].encode('utf8') + ']', level = log.DEBUG)
                else:
                    log.msg(attr_name + " None", level = log.DEBUG)
        except:
            exstr = traceback.format_exc()
            log.msg('failed to get attr_name [' + attr_name + '] ' + exstr, level = log.ERROR)
            return None
    return attr_dict

def get_default_end_time():
    end_time_str = str(datetime.now().date()) + " 23:59:59"
    end_time = int(datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
    return end_time

def get_default_start_time():
    start_time_str = str(datetime.now().date()) + " 00:00:00"
    start_time = int(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
    return start_time

def find_element_by_xpath(driver, xpath, log_level = log.ERROR):
    try:
        a_obj = driver.find_element_by_xpath(xpath)
        return a_obj
    except NoSuchElementException:
        exstr = traceback.format_exc()
        log.msg('failed to find_element_by_xpath ' + xpath + ' NoSuchElementException ' + exstr, level = log_level)
        return None
    except:
        exstr = traceback.format_exc()
        log.msg('failed to find_element_by_xpath ' + xpath + ' ' + exstr, level = log_level)
        return None

def find_elements_by_xpath(driver, xpath, log_level = log.ERROR):
    try:
        a_objs = driver.find_elements_by_xpath(xpath)
        return a_objs
    except NoSuchElementException:
        exstr = traceback.format_exc()
        log.msg('failed to find_elements_by_xpath ' + xpath + ' NoSuchElementException' + exstr, level = log_level)
        return None
    except:
        exstr = traceback.format_exc()
        log.msg('failed to find_elements_by_xpath ' + xpath + ' ' + exstr, level = log_level)
        return None

def driver_quit(driver, log_level = log.ERROR):
    try:
        driver.quit()
    except:
        exstr = traceback.format_exc()
        log.msg('failed to driver.quit() ' + exstr, level = log_level)

def click_url(driver, xpath):
    try:
        a_obj = find_element_by_xpath(driver, xpath)
        if not a_obj:
            return None
        a_obj.click()
        time.sleep(2)

        url = driver.current_url
    except:
        exstr = traceback.format_exc()
        log.msg('failed when chick url xpath ' + xpath + ' ' + str(exstr), level = log.WARNING)
        return None
    return url

def click_a_obj(driver, a_obj):
    try:
        if not a_obj:
            return None
        a_obj.click()
        time.sleep(2)

        url = driver.current_url
    except:
        exstr = traceback.format_exc()
        log.msg('failed when chick a_obj ' + str(exstr), level = log.WARNING)
        return None
    return url

def execute_script(driver, command):
    try:
        driver.execute_script(command)
    except:
        exstr = traceback.format_exc()
        log.msg('failed when execute_script ' + command + str(exstr), level = log.WARNING)
        return False
    return True
def is_item_changed(item, cursor):
    if not cursor:
        return True
    elif cursor['ori_price'] != item['ori_price']:
        return True
    elif cursor['cur_price'] != item['cur_price']:
        return True
    return False

def check_url(url):
    try:
        a = urllib2.urlopen(url)
    except:
        exstr = traceback.format_exc()
        log.msg('failed to get url ' + str(exstr), level = log.WARNING)
        return False, 0
    return True, a.getcode()

def get_string(item, key):
    value = item[key]
    if value.__class__.__name__ == 'list':
        info = ''
        for i in xrange(len(value)):
            #if i > 0:
            #    info = info + ' '
            info = info + value[i]
        return info
    else:
        return value

def async_get_cats_info(type):
    op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
    params = {
        'method':'taobao.topats.itemcats.get',
        'output_format':'json',
        'cids': '0',
        'type': type,
    }
    dict_str = op.get_result(params)
    ret_dict = json.loads(dict_str)
    return ret_dict

def async_get_result(taskid):
    op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
    params = {
        'method':'taobao.topats.result.get',
        'task_id': taskid,
    }
    dict_str = op.get_result(params)
    ret_dict = json.loads(dict_str)
    return ret_dict

def get_root_cid():
    op = OpenTaobao('12651461','80a15051c411f9ca52d664ebde46a9da')
    params = {
        'method':'taobao.itemcats.get',
        'fields':'name, cid',
        'parent_cid': '0',
    }
    dict_str = op.get_result(params)
    ret_dict = json.loads(dict_str)
    return ret_dict

def download_result(taskid, download_file):
    while True:
        ret_dict = async_get_result(taskid)
        if ret_dict.has_key('topats_result_get_response') and ret_dict['topats_result_get_response']['task']['status'] == 'done':
            url = ret_dict['topats_result_get_response']['task']['download_url']

            form_data = urllib.urlencode({})
            buffer = urllib2.urlopen(url, form_data).read()
            file = open(download_file, 'w')
            file.write(buffer)
            file.close()
            break
        else:
            time.sleep(10)

def get_cats_info(type, download_file):
    ret_dict = async_get_cats_info(type)
    #print 'ret_dict ' + str(ret_dict)
    if ret_dict.has_key('topats_itemcats_get_response'):
        taskid = ret_dict['topats_itemcats_get_response']['task']['task_id']
    elif ret_dict.has_key('error_response'):
        sub_msg = ret_dict['error_response']['sub_msg']
        taskid = get_task_id(sub_msg)
        if not taskid:
            return
        #print 'taskid ' + str(taskid)
    async_ret_dict = async_get_result(taskid)
    #print 'async_ret_dict ' + str(async_ret_dict)
    download_result(taskid, download_file)
        

def build_root_leave_dict(origin_cat_dict, root_leave_dict, level = 0):
    if not origin_cat_dict.has_key('cid'):
        return
    if not origin_cat_dict['cid']:
        return
    cid = origin_cat_dict['cid']
    if not root_leave_dict.has_key(cid):
        root_leave_dict[cid] = {}

    if not origin_cat_dict.has_key('childCategoryList'):
        return
    if not origin_cat_dict['childCategoryList']:
        return
    #print 'origin_cat_dict.__class__.__name__ ' + origin_cat_dict.__class__.__name__ + " " + str(root_leave_dict)
    try:
        #print 'level ' + str(level) + ' ' + str(len(origin_cat_dict['childCategoryList']))
        for item in origin_cat_dict['childCategoryList']:
            sub_cid = item['cid']
            root_leave_dict[cid][sub_cid] = {}
            build_root_leave_dict(item, root_leave_dict[cid], level + 1)
    except:
        exstr = traceback.format_exc()
        log.msg('failed to build_root_leave_dict ' + exstr, level = log.WARNING)
        return 

def build_cat_tree(dir_list):
    root_leave_dict = {}
    for dir in dir_list:
        files = os.listdir(dir)
        #print 'files : ' + str(files)
        i = 0
        for file in files:
            path=dir + '/' + file
            f = open(path, 'r')
            #print 'open ' + path
            buffer = f.read()
            ret_dict = json.loads(buffer)
            build_root_leave_dict(ret_dict, root_leave_dict)
            i = i + 1

        #print 'root_leave_dict ' + str(root_leave_dict)
        return root_leave_dict

def build_cat_map(root_leave_dict, root_cid, map_dict):

    for cid in root_leave_dict:
        if len(root_leave_dict[cid]) == 0:
            map_dict[cid] = root_cid
        else:
            build_cat_map(root_leave_dict[cid], root_cid, map_dict)

def build_cat_total_map(root_leave_dict):
    map_dict = {}
    for cid in root_leave_dict:
        build_cat_map(root_leave_dict[cid], cid, map_dict)

    return map_dict
g_cid_map = {
        u'服饰箱包':u'穿的', 
        u'珠宝首饰':u'穿的', 
        u'鞋靴':u'穿的', 
        u'男装':u'穿的', 
        u'运动服/休闲服装':u'穿的', 
        u'流行男鞋':u'穿的', 
        u'女装/女士精品':u'穿的', 
        u'女鞋':u'穿的', 
        u'箱包皮具/热销女包/男包':u'穿的', 
        u'女士内衣/男士内衣/家居服':u'穿的', 
        u'服饰配件/皮带/帽子/围巾':u'穿的', 
        u'珠宝/钻石/翡翠/黄金':u'穿的', 
        u'运动鞋new':u'穿的', 
        u'饰品/流行首饰/时尚饰品新':u'穿的', 
        u'手表':u'穿的', 
        u'运动包/户外包/配件':u'穿的',

        u'食品':u'吃的',
        u'餐饮美食': u'吃的',
        u'零食/坚果/特产': u'吃的',
        u'粮油米面/南北干货/调味品' : u'吃的',
        u'茶/咖啡/冲饮':u'吃的',
        u'水产肉类/新鲜蔬果/熟食':u'吃的',
        u'酒类':u'吃的',

        u'小家电':u'数码/家电', 
        u'数码影音':u'数码/家电', 
        u'手机/通讯':u'数码/家电', 
        u'电视、音响':u'数码/家电', 
        u'电脑用品':u'数码/家电', 
        u'国货精品数码':u'数码/家电', 
        u'手机':u'数码/家电', 
        u'数码相机/单反相机/摄像机':u'数码/家电', 
        u'MP3/MP4/iPod/录音笔':u'数码/家电', 
        u'笔记本电脑':u'数码/家电', 
        u'平板电脑/MID':u'数码/家电', 
        u'台式机/一体机/服务器':u'数码/家电', 
        u'电脑硬件/显示器/电脑周边':u'数码/家电', 
        u'网络设备/网络相关':u'数码/家电', 
        u'3C数码配件':u'数码/家电', 
        u'闪存卡/U盘/存储/移动硬盘':u'数码/家电', 
        u'办公设备/耗材/相关服务':u'数码/家电', 
        u'电子词典/电纸书/文化用品':u'数码/家电', 
        u'电玩/配件/游戏/攻略':u'数码/家电', 
        u'大家电':u'数码/家电', 
        u'影音电器':u'数码/家电', 
        u'生活电器':u'数码/家电', 
        u'厨房电器':u'数码/家电',

        u'个护健康':u'日用品', 
        u'家居':u'日用品', 
        u'家居装修':u'日用品', 
        u'钟表':u'日用品', 
        u'厨具':u'日用品', 
        u'住宅家具':u'日用品', 
        u'居家日用/婚庆/创意礼品':u'日用品', 
        u'厨房/餐饮用具':u'日用品', 
        u'清洁/卫浴/收纳/整理用具':u'日用品', 
        u'床上用品/布艺软饰':u'日用品', 
        u'洗护清洁剂/卫生巾/纸/香薰':u'日用品', 

        u'彩妆/香水/美妆工具':u'化妆品',
        u'美容护肤/美体/精油':u'化妆品',
        u'美发护发/假发':u'化妆品',

        }
def get_root_cid_map():
    ret_dict = get_root_cid()
    root_cid_map = {}
    if ret_dict.has_key('itemcats_get_response'):
        for item in ret_dict['itemcats_get_response']['item_cats']['item_cat']:
            cid = item['cid']
            name = item['name']

            if g_cid_map.has_key(name):
                root_cid_map[cid] = {'origin_category_name' : name, 'category_name' : g_cid_map[name]}
            else:
                root_cid_map[cid] = {'origin_category_name' : name, 'category_name' : u'其它'}
    return root_cid_map

def get_url_content(url):
    try:
        params = {}
        form_data = urllib.urlencode(params)
        buffer = urllib2.urlopen(url, form_data).read()
        return buffer
    except:
        exstr = traceback.format_exc()
        log.msg('failed to get_url_content ' + url + ' ' + exstr, level = log.WARNING)
        return None 

class CategoryGet:
    def __init__(self, dir_list):
        self.root_cid_map = get_root_cid_map() 
        self.root_dict = build_cat_tree(dir_list)
        self.map_dict = build_cat_total_map(self.root_dict)

    def get_cid_name(self, cid):
        if self.map_dict.has_key(cid):
            root_cid = self.map_dict[cid]
            if self.root_cid_map.has_key(root_cid):
                return self.root_cid_map[root_cid]['origin_category_name'], self.root_cid_map[root_cid]['category_name']
        return u'其它', u'其它'

    def tranverse(self):
        for key in self.map_dict:
            print str(key) + ' -> ' + self.get_cid_name(key).encode('utf8')

g_zseckill_category_map = {
        u'鞋靴':u'穿的',
        u'服饰箱包':u'穿的',

        u'食品':u'吃的',

        u'小家电':u'数码/家电', 
        u'数码影音':u'数码/家电',
        u'手机/通讯':u'数码/家电',
        u'电视、音响':u'数码/家电',
        u'电脑用品':u'数码/家电',

        u'家居':u'日用品',
        u'钟表':u'日用品',
        u'运动户外休闲':u'日用品',

        u'珠宝首饰':u'化妆品',

        u'汽车用品':u'其它',
        u'图书':u'其它',
        u'乐器':u'其它',
        u'家居装修':u'其它',
        u'玩具':u'其它',
        u'宠物用品':u'其它',
        u'厨具':u'其它',
        u'个护健康':u'其它',
        u'母婴用品':u'其它',

        }
def get_zseckill_cateogry_name(origin_category_name):
    if g_zseckill_category_map.has_key(origin_category_name):
        return g_zseckill_category_map[origin_category_name]
    else:
        return u'其它'

if __name__ == '__main__':
    #get_cats_info('1', 'download.txt')
    #root_dict = build_cat_tree(['1', '2'])
    #map_dict = build_cat_total_map(root_dict)
    #for key in map_dict:
    #    print str(key) + ' -> ' + str(map_dict[key])
    #print str(get_root_cid())
    cg = CategoryGet(['1', '2'])
    cg.tranverse()
