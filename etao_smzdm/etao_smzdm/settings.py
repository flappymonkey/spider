# Scrapy settings for template project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'template'

SPIDER_MODULES = ['etao_smzdm.spiders']
NEWSPIDER_MODULE = 'etao_smzdm.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'template (+http://www.yourdomain.com)'
ITEM_PIPELINES=['etao_smzdm.pipelines.EtaoSmzdmPipeline']
#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy'
MONGODB_COLLECTION = 'etao_smzdm_temp'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
