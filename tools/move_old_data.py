#encoding=utf8
__author__ = 'luoyan@maimiaotech.com'


import sys
import os
import datetime

curr_path = os.path.dirname(__file__)
sys.path.append(os.path.join(curr_path,'../../'))

import pymongo
if pymongo.version.startswith("2.5"):
    import bson.code
    pymongo.code = bson.code
    sys.modules['pymongo.code'] = bson.code
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
from pymongo import Connection
mongoConn = Connection(host = MONGODB_HOST, port = MONGODB_PORT)
import datetime
import logging
import logging.config
logging.config.fileConfig('../conf/consolelogger_move_old_data.conf')
logger = logging.getLogger(__name__)

class OldSeckills(object):
    """
    class to operate cold_query  
    """
    _conn = mongoConn
    _db = 'seckills'
    _coll = 'old_seckill'
    coll = _conn[_db][_coll]

    @classmethod
    def scan(cls):
        try:
            cursor = cls.coll.find()
        except Exception,e:
            logger.debug('scan error : %s'%(e))
            return None
        return cursor

    @classmethod
    def remove(cls, item):
        try:
            cursor = cls.coll.remove({'_id':item['_id']})
        except Exception,e:
            logger.debug('scan error : %s'%(e))

    @classmethod
    def save(cls, item):
        cls.coll.update({'id': item['id']}, item, True)

class Seckills(object):
    """
    class to operate cold_query  
    """
    _conn = mongoConn
    _db = 'seckills'
    _coll = 'seckill'
    coll = _conn[_db][_coll]

    @classmethod
    def scan(cls):
        try:
            cursor = cls.coll.find()
        except Exception,e:
            logger.debug('scan error : %s'%(e))
            return None
        return cursor

    @classmethod
    def remove(cls, item):
        try:
            cursor = cls.coll.remove({'_id':item['_id']})
        except Exception,e:
            logger.debug('scan error : %s'%(e))

    @classmethod
    def save(cls, item):
        cls.coll.update({'id': item['id']}, item, True)


class OldZtmhs(object):
    """
    class to operate cold_query  
    """
    _conn = mongoConn
    _db = 'scrapy'
    _coll = 'old_ztmhs'
    coll = _conn[_db][_coll]

    @classmethod
    def scan(cls):
        try:
            cursor = cls.coll.find()
        except Exception,e:
            logger.debug('scan error : %s'%(e))
            return None
        return cursor

    @classmethod
    def save(cls, item):
        cls.coll.update({'id': item['id']}, item, True)

    @classmethod
    def remove(cls, item):
        try:
            cursor = cls.coll.remove({'_id':item['_id']})
        except Exception,e:
            logger.debug('remove error : %s'%(e))

class Ztmhs(object):
    """
    class to operate cold_query  
    """
    _conn = mongoConn
    _db = 'scrapy'
    _coll = 'ztmhs'
    coll = _conn[_db][_coll]

    @classmethod
    def scan(cls):
        try:
            cursor = cls.coll.find()
        except Exception,e:
            logger.debug('scan error : %s'%(e))
            return None
        return cursor

    @classmethod
    def remove(cls, item):
        try:
            cursor = cls.coll.remove({'_id':item['_id']})
        except Exception,e:
            logger.debug('remove error : %s'%(e))

    @classmethod
    def save(cls, item):
        cls.coll.update({'id': item['id']}, item, True)

class MoveOldData:

    def __init__(self, table, old_table, before_seconds, real_move):
        self.table = table
        self.old_table = old_table
        self.before_seconds = before_seconds
        self.real_move = real_move

    def is_old_item(self, item):
        return True, True

    def move(self):
        logger.info('start to move old data')
        cursor = self.table.scan()
        if not cursor:
            return
        i = 0
        total = 0
        no_time = 0
        real_remove = 0
        for item in cursor:
            total = total + 1
            has_time, old_time = self.is_old_item(item)
            if not has_time:
                no_time = no_time + 1
                continue
            if not old_time:
                continue
            self.old_table.save(item)
            i = i + 1
            if self.real_move:
                self.table.remove(item)
                real_remove = real_remove + 1
        logger.info('end to move old data ' + str(i) + ' no_time ' + str(no_time) + ' total ' + str(total) + ' real_remove ' + str(real_remove))

    def recover(self):
        logger.info('start to recover old data')
        cursor = self.old_table.scan()
        if not cursor:
            return
        i = 0
        total = 0
        no_time = 0
        real_remove = 0
        for item in cursor:
            total = total + 1
            self.table.save(item)
            i = i + 1
            if self.real_move:
                self.old_table.remove(item)
                real_remove = real_remove + 1
        logger.info('end to move old data ' + str(i) + ' no_time ' + str(no_time) + ' total ' + str(total) + ' real_remove ' + str(real_remove))

class SeckillMovOldData(MoveOldData):
    
    def __init__(self, before_seconds, real_move):
        MoveOldData.__init__(self, Seckills, OldSeckills, before_seconds, real_move)

    def is_old_item(self, item):
        if not item.has_key('display_time_end'):
            has_time = False
            old_time = False
            return has_time, old_time
            
        has_time = True
        delta = int(datetime.datetime.now().strftime("%s")) - item['display_time_end']
        if delta > self.before_seconds:
            old_time = True
        else:
            old_time = False
        return has_time, old_time

class ZtmhsMovOldData(MoveOldData):

    def __init__(self, before_seconds, real_move):
        MoveOldData.__init__(self, Ztmhs, OldZtmhs, before_seconds, real_move)

    def is_old_item(self, item):
        if not item.has_key('pub_time'):
            has_time = False
            old_time = False
            return has_time, old_time
        
        end_time_str = str(datetime.datetime.now().date()) + " 00:00:00"
        end_time = int(datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
        pub_time_str = item['pub_time']
        #print 'pub_time_str [' + pub_time_str + ']'
        has_time = True
        if pub_time_str == "":
            logger.warning('failed to get pub_time [' + str(pub_time_str) + '] ')
            old_time = False
        else:
            try:
                pub_time = int(datetime.datetime.strptime(pub_time_str, "%Y-%m-%d %H:%M:%S").strftime("%s"))
            except:
                exstr = traceback.format_exc()
                logger.warning('failed to get pub_time [' + str(pub_time_str) + '] ' + exstr)
                old_time = False
                return has_time, old_time
            if end_time - pub_time > self.before_seconds:
                old_time = True
                if not self.real_move:
                    logger.info('try to move pub_time_str [' + pub_time_str + ']')
            else:
                old_time = False

        return has_time, old_time

def usage(argv0):
    print argv0 + " before_days = 7 seckill/ztmhs realmove=1/0 recover=0/1"
if __name__ == '__main__':
    if len(sys.argv) > 5:
        usage(sys.argv[0])
        sys.exit(0)
    if len(sys.argv) == 1:
        days = 7
        db_type = 'seckill'
        real_move = True
        recover = False
    elif len(sys.argv) == 2:
        days = int(sys.argv[1])
        db_type = 'seckill'
        real_move = True
        recover = False
    elif len(sys.argv) == 3:
        days = int(sys.argv[1])
        db_type = sys.argv[2]
        real_move = True
        recover = False
    elif len(sys.argv) == 4:
        days = int(sys.argv[1])
        db_type = sys.argv[2]
        real_move = True
        recover = False
    else:
        days = int(sys.argv[1])
        db_type = sys.argv[2]
        if sys.argv[3] == '1':
            real_move = True
        else:
            real_move = False
        if sys.argv[4] == '1':
            recover = True
        else:
            recover = False

    if db_type == 'seckill':
        m = SeckillMovOldData(3600 * 24 * days, real_move)
    else:
        m = ZtmhsMovOldData(3600 * 24 * days, real_move)
    if recover:
        m.recover()
    else:
        m.move()
    #move_old_data(3600 * 24 * days)
