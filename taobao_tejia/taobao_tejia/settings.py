# Scrapy settings for taobao_tejia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'taobao_tejia'

SPIDER_MODULES = ['taobao_tejia.spiders']
NEWSPIDER_MODULE = 'taobao_tejia.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobao_tejia (+http://www.yourdomain.com)'
#WEBKIT_DOWNLOADER=['taobao_tejia']
#DOWNLOADER_MIDDLEWARES = {
#        'taobao_tejia.middleware.WebkitDownloader': 1,
#}
import os
os.environ["DISPLAY"] = ":0"
ITEM_PIPELINES=['taobao_tejia.pipelines.TaobaoTejiaPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
