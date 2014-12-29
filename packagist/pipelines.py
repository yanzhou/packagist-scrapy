# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from packagist.items import PackageItem, PackageBriefItem, UserItem, UserStarredPackagesItem
from pymongo import MongoClient


class MongoStorePipeline(object):
    """
    store items to mongodb
    """
    def __init__(self):
        """
        config mongodb connection
        """
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.packagist

    def process_item(self, item, spider):
        if isinstance(item, PackageItem):
            self.store_package(item)

    def store_package(self, item):
        """
        save full info of package
        """
        conditions = {
            'vendor': item['vendor'],
            'name': item['name']
        }
        self.db.packages.update(conditions, dict(item), True)