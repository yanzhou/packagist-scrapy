# -*- coding: utf-8 -*-

# Scrapy settings for PackagistScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'packagist'

SPIDER_MODULES = ['packagist.spiders']
NEWSPIDER_MODULE = 'packagist.spiders'
ITEM_PIPELINES = {
    'packagist.pipelines.MongoStorePipeline': 300,
}

CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 0.25
DOWNLOAD_TIMEOUT = 3600
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'log.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PackagistScrapy (+http://www.yourdomain.com)'
