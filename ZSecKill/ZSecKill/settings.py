#coding=utf-8

BOT_NAME = 'ZSecKill'

SPIDER_MODULES = ['ZSecKill.spiders']
NEWSPIDER_MODULE = 'ZSecKill.spiders'
ITEM_PIPELINES=['ZSecKill.pipelines.ZseckillPipeline']

START_URL = ['http://www.amazon.cn/%E4%BF%83%E9%94%80-%E7%89%B9%E4%BB%B7/b/ref=cs_top_nav_gb27?ie=UTF8&node=42450071']
TIME_OUT = 20
#LOG_FILE='zseckill.log'
#LOG_LEVEL='DEBUG'

#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ZSecKill (+http://www.yourdomain.com)'
