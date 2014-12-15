# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PackageItem(scrapy.Item):
    """
    Package information
    """
    # vendor name
    vendor = scrapy.Field()
    # package name
    name = scrapy.Field()
    # tags, list
    tags = scrapy.Field()
    # downloads info, including number of installs of overall, 30-days and today
    downloads = scrapy.Field()
    # number of stars
    stars = scrapy.Field()
    # description
    description = scrapy.Field()
    # details info, including urls of maintainers, homepage, canonical, source, issues, IRC and so on
    details = scrapy.Field()
    # detailed versions info
    # including version tag, source-reference, release-data, licence, authors, requires, devRequires, suggests,
    # provides, conflicts and replaces
    # type: dict, version tag as the key
    versions = scrapy.Field()


class PackageBriefItem(scrapy.Item):
    """
    Brief information of package, used to crawl package info form the list page
    """
    # vendor name
    vendor = scrapy.Field()
    # package name
    name = scrapy.Field()
    # downloads info, including number of installs of overall, 30-days and today
    downloads = scrapy.Field()
    # number of stars
    stars = scrapy.Field()


class UserItem(scrapy.Item):
    """
    User information
    """
    # username
    username = scrapy.Field()
    # register date
    register_date = scrapy.Field()


class UserStarredPackagesItem(scrapy.Item):
    """
    packages which have been starred by user
    """
    # username
    username = scrapy.Field()
    # packages that user stars
    # url sample: https://packagist.org/users/Seldaek/favorites/
    # type: dict, 'vendor', 'name'
    starred = scrapy.Field()