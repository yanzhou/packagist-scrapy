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
        if isinstance(item, PackageBriefItem):
            self.store_package_brief(item)
        elif isinstance(item, PackageItem):
            self.store_package(item)
        elif isinstance(item, UserItem):
            self.store_user(item)
        elif isinstance(item, UserStarredPackagesItem):
            self.store_user_starred_packages(item)
        raise DropItem("item saved successfully")

    def store_package_brief(self, item):
        """
        save brief info of package
        """
        self.db.packages.insert(dict(item))

    def store_package(self, item):
        """
        save full info of package
        """
        conditions = {
            'vendor': item['vendor'],
            'name': item['name']
        }
        self.db.packages.update(conditions, dict(item))

    def store_user(self, item):
        """
        save user info
        """
        self.db.users.insert(dict(item))

    def store_user_starred_packages(self, item):
        """
        save packages which have been starred by user
        """
        conditions = {
            'username': item['username']
        }
        self.db.packages.update(conditions, dict(item))