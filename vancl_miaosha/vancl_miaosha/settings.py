# Scrapy settings for vancl_miaosha project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vancl_miaosha'

SPIDER_MODULES = ['vancl_miaosha.spiders']
NEWSPIDER_MODULE = 'vancl_miaosha.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vancl_miaosha (+http://www.yourdomain.com)'
ITEM_PIPELINES=['vancl_miaosha.pipelines.VanclMiaoshaPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
