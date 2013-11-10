# Scrapy settings for etao_9kuai9 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'etao_9kuai9'

SPIDER_MODULES = ['etao_9kuai9.spiders']
NEWSPIDER_MODULE = 'etao_9kuai9.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'etao_9kuai9 (+http://www.yourdomain.com)'
ITEM_PIPELINES=['etao_9kuai9.pipelines.Etao9Kuai9Pipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'seckills'
MONGODB_COLLECTION = 'seckill'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
