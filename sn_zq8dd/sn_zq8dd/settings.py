# Scrapy settings for sn_zq8dd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sn_zq8dd'

SPIDER_MODULES = ['sn_zq8dd.spiders']
NEWSPIDER_MODULE = 'sn_zq8dd.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sn_zq8dd (+http://www.yourdomain.com)'
ITEM_PIPELINES=['sn_zq8dd.pipelines.SnZq8DdPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
