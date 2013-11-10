#encoding=utf8
__author__ = 'luoyan@maimiaotech.com'


import sys
import os
import datetime

curr_path = os.path.dirname(__file__)
sys.path.append(os.path.join(curr_path,'../../'))
from search.db_models.smzdm import Smzdm
from search.db_models.smzdm_tmp import SmzdmTmp
from search.db_models.etao_smzdm_tmp import EtaoSmzdmTmp
import logging
import logging.config
logging.config.fileConfig('../conf/consolelogger_detect_data.conf')
logger = logging.getLogger(__name__)
sys.path.append(os.path.join(curr_path,'../../Spider/comm_lib'))
import utils
import hashlib

class DetectDuplicate:

    def __init__(self, table, real_remove):
        self.table = table
        self.real_remove = real_remove

    def get_hash_code(self, item):
        title = utils.get_string(item, 'title')
        hash_code = hashlib.md5(title.encode('utf8')).hexdigest()
        return hash_code

    def is_new_id(self, item, hash_dict):
        hash_code = self.get_hash_code(item)
        has_same_title = False
        if not hash_dict['title'].has_key(hash_code) or len(hash_dict['title'][hash_code]) == 0:
            has_same_title = False
            return True, has_same_title, None

        has_same_title = True
        id_list = []
        for sub_item in hash_dict['title'][hash_code]:
            id_list.append([sub_item['id'], sub_item['source_url']])
            if sub_item['id'] == item['id']:
                return False, has_same_title, id_list
        return True, has_same_title, id_list

    def add_item(self, item, hash_dict):
        hash_code = self.get_hash_code(item)
        if not hash_dict['title'].has_key(hash_code):
            hash_dict['title'][hash_code] = []
        hash_dict['title'][hash_code].append(item)

    def build(self):
        cursor = self.table.scan()
        hash_dict = {}
        hash_dict['title'] = {}
        for item in cursor:
            self.add_item(item, hash_dict)
        return hash_dict

    def get_earliest(self, items):
        if len(items) == 0:
            logger.error('len(items) == 0')
            return None, None

        min_pub_time = 0
        min_pub_time_id = None
        title = None
        for item in items:
            pub_time_str = item['pub_time']
            pub_time = int(datetime.datetime.strptime(pub_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
            if not min_pub_time_id: 
                min_pub_time = pub_time
                min_pub_time_id = item['id']
                title = utils.get_string(item, 'title')
            elif min_pub_time > pub_time:
                min_pub_time = pub_time
                min_pub_time_id = item['id']
                title = utils.get_string(item, 'title')

        return min_pub_time_id, title

    def reduce(self):
        hash_dict = self.build()
        dict = hash_dict['title']
        for hash_code in dict:
            items = dict[hash_code]
            if len(items) > 1:
                min_pub_time_id, title = self.get_earliest(items)             
                for item in items:
                    link = ""
                    if item.has_key('link'):
                        link = item['link']
                    if item['id'] != min_pub_time_id:
                        if self.real_remove:
                            self.table.remove(item)
                        logger.info('remove duplicate item id ' + str(item['id']) + ' title ' + str(title.encode('utf8')) + ' pub_time ' + str(item['pub_time']) + ' source_url ' + str(item['source_url']) + ' link ' + link)
                    else:
                        logger.info('reserve duplicate item id ' + str(item['id']) + ' title ' + str(title.encode('utf8')) + ' pub_time ' + str(item['pub_time']) + ' source_url ' + str(item['source_url']) + ' link ' + link)

class DetectData:
    default_url = '/static/upload_images/badimg.png'

    def __init__(self, src_table, dest_table, real_move, slice, partition_num):
        self.src_table = src_table
        self.dest_table = dest_table
        self.real_move = real_move
        self.slice = slice
        self.partition_num = partition_num
        self.detect_duplicate = DetectDuplicate(dest_table, real_move)
        self.hash_dict = self.detect_duplicate.build()

    def check_url(self, url):
        valid, code = utils.check_url(url)
        if not valid:
            logger.warning('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + ' failed to get url '+ url)
            to_add_url = self.default_url
            change = True
        elif code == 200:
            logger.info('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + ' code ' + str(code) + ' ' + url)
            to_add_url = url
            change = False
        else:
            logger.waring('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + 'failed to get url ' + url + ' retcode ' + str(code))
            to_add_url = self.default_url
            change = True
        return to_add_url, change

    def valid_url(self, url):
        if url.find('pn.zdmimg.com') != -1:
            logger.warning('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + ' ' + url + ' replace to ' + self.default_url)
            return self.default_url, False
        logger.info('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + ' ' + url)
        return url, True
            

    def detect_item(self, item):
        img_url_list = []
        change = False
        for url in item['img']:
            '''
            to_add_url, need_change = self.check_url(url)
            if need_change:
                change = True
            else:
            '''
            to_add_url, valid = self.valid_url(url)
            if not valid:
                change = True
            img_url_list.append(to_add_url)
        if change:
            item['img'] = img_url_list
        if not self.check_duplicate(item):
            return False
        return True

    def check_duplicate(self, item):
        is_new_id, has_same_title, id_list = self.detect_duplicate.is_new_id(item, self.hash_dict)
        if has_same_title and is_new_id:
            logger.info('skip duplicate url id = ' + item['id'] + ' source_url ' + item['source_url'] + ' origin_id ' + str(id_list))
            return False

        self.detect_duplicate.add_item(item, self.hash_dict)
        return True

    def detect(self):
        logger.info('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + ' start to detect data')
        cursor = self.src_table.scan()
        if not cursor:
            return
        i = 0
        total = 0
        real_remove = 0
        duplicate = 0
        for item in cursor:
            id = int(item['id'], 16)
            if id % self.partition_num != self.slice:
                continue
            total = total + 1
            if not self.detect_item(item):
                duplicate = duplicate + 1
                continue

            self.dest_table.save(item)
            i = i + 1
            if self.real_move:
                self.src_table.remove(item)
                real_remove = real_remove + 1
        logger.info('slice ' + str(self.slice) + ' partition_num ' + str(self.partition_num) + ' end to detect data ' + str(i) + ' total ' + str(total) + ' real_remove ' + str(real_remove) + ' duplicate ' + str(duplicate))

    def recover(self):
        logger.info('start to recover old data')
        cursor = self.dest_table.scan()
        if not cursor:
            return
        i = 0
        total = 0
        no_time = 0
        real_remove = 0
        for item in cursor:
            total = total + 1
            self.src_table.save(item)
            i = i + 1
            if self.real_move:
                self.dest_table.remove(item)
                real_remove = real_remove + 1
        logger.info('end to move old data ' + str(i) + ' no_time ' + str(no_time) + ' total ' + str(total) + ' real_remove ' + str(real_remove))

def usage(argv0):
    print argv0 + ' detect smzdm/etao_smzdm slice[0-9] partition_num=10'
    print argv0 + ' detectmove smzdm/etao_smzdm slice[0-9] partition_num=10'
    print argv0 + ' duplicatemove smzdm/etao_smzdm slice[0-9] partition_num=10'
    print argv0 + ' duplicate smzdm/etao_smzdm slice[0-9] partition_num=10'

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage(sys.argv[0])
        sys.exit(-1)
    slice = int(sys.argv[3])
    partition_num = int(sys.argv[4])
    if sys.argv[1] == 'detect' or sys.argv[1] == 'duplicate':
        move = False
    elif sys.argv[1] == 'detectmove' or sys.argv[1] == 'duplicatemove':
        move = True
    else:
        usage(sys.argv[0])
        sys.exit(-1)

    if sys.argv[2] == 'smzdm':
        src_table = SmzdmTmp
    elif sys.argv[2] == 'etao_smzdm':
        src_table = EtaoSmzdmTmp
    else:
        usage(sys.argv[0])
        sys.exit(-1)
    if sys.argv[1] == 'detect' or sys.argv[1] == 'detectmove':
        dd = DetectData(src_table, Smzdm, move, slice, partition_num)
        dd.detect()
    elif sys.argv[1] == 'duplicate' or sys.argv[1] == 'duplicatemove':
        dd = DetectDuplicate(Smzdm, move)
        dd.reduce()
    else:
        usage(sys.argv[0])
        sys.exit(-1)
        #dd = DetectData(SmzdmTmp, Smzdm, False)
        #dd.check_url('http://pn.zdmimg.com/201311/02/1dc87af1.jpg_n4.jpg')
