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
    # html of package detail page for later processing in case error occurs
    html = scrapy.Field()
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