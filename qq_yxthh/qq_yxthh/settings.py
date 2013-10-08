# Scrapy settings for qq_yxthh project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'qq_yxthh'

SPIDER_MODULES = ['qq_yxthh.spiders']
NEWSPIDER_MODULE = 'qq_yxthh.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qq_yxthh (+http://www.yourdomain.com)'
#WEBKIT_DOWNLOADER=['qq_yxthh']
#DOWNLOADER_MIDDLEWARES = {
#    'qq_yxthh.middleware.WebkitDownloader': 1,
#}
import os
#os.environ["DISPLAY"] = ":3"
ITEM_PIPELINES=['qq_yxthh.pipelines.QqYxthhPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
