#coding=utf-8

import sys
import json
from urllib import unquote

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_list_merge(cur_list):
    cur_str = ''
    if cur_list:
        for item in cur_list:
            cur_str = cur_str + item + ' '
        return cur_str[:-1]
    else:
        return ''
def parse_list_url(cur_list):
    cur_str = ''
    if cur_list:
        for temp_list in cur_list:
            cur_str = cur_str + temp_list[0] + ':' + unquote(temp_list[1]) + '\n'
        return cur_str[:-1]
    else:
        return ''
def parse_list(cur_list):
    cur_str = ''
    if cur_list:
        for item in cur_list:
            cur_str = cur_str + item + '\n'
        return cur_str[:-1]
    else:
        return ''
def parse_dict_url(cur_dict):
    cur_str = ''
    if cur_dict:
        for (key,value) in cur_dict.items():
            cur_str = cur_str + key + ':' + unquote(value) + '\n'
        return cur_str[:-1]
    else:
        return ''


def parse_item(item):
    print '----------------------------------------------------------------------------'
    print 'ID: ',item['id']
    print '抓取来源: ',item['crawl_source']
    print '原始url: ',item['source_url']
    print '商城: ',parse_list(item['source'])
    print '标题: ',parse_list_merge(item['title'])
    print '描述: ',parse_list(item['desc'])
    print '链接: ',parse_list_url(item['desc_link_list'])
    print '直达链接: ',parse_list_url(item['go_link'])
    print '图片: ',parse_list(item['img'])
    print '分类: ',parse_list(item['cat'])
    print '更新时间: ',item['pub_time']
    print '值得人数: ',item['worth_num']
    print '不值得人数: ',item['bad_num']
if __name__ == "__main__":
    f = open(sys.argv[1],'r')
    for line in f:
        line = line[:-1]
        #print line
        item = json.loads(line)
        parse_item(item)