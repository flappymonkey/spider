# Scrapy settings for newegg_zhadan project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newegg_zhadan'

SPIDER_MODULES = ['newegg_zhadan.spiders']
NEWSPIDER_MODULE = 'newegg_zhadan.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newegg_zhadan (+http://www.yourdomain.com)'
ITEM_PIPELINES=['newegg_zhadan.pipelines.NeweggZhadanPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
