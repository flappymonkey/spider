# Scrapy settings for taobao_jhs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'taobao_jhs'

SPIDER_MODULES = ['taobao_jhs.spiders']
NEWSPIDER_MODULE = 'taobao_jhs.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobao_jhs (+http://www.yourdomain.com)'
ITEM_PIPELINES=['taobao_jhs.pipelines.TaobaoJhsPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
