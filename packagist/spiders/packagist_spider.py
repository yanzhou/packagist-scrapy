import scrapy
from packagist.items import PackageItem
from scrapy.selector import Selector


class PackagistSpider(scrapy.Spider):
    name = 'packagist'
    allowed_domains = ["packagist.org"]
    start_urls = ["https://packagist.org/explore/popular"]

    def parse(self, response):
        """
        parse the list page
        """
        # current page
        current_page = int(response.xpath('//nav/span[@class="current"]/text()').extract()[0])
        # text of the last a link of nav tag, if it is not the last page, then the last a link of nav tag is next page,
        # or it is previous page
        next_page = int(response.xpath('//nav/a[last()]/@href').extract()[0].split('=')[1])
        if current_page < next_page:
            url = "https://packagist.org/explore/popular?page=" + str(next_page)
            # generate request to download list pages
            yield scrapy.Request(url, callback=self.parse)

        # package urls
        package_urls = response.xpath('//ul[@class="packages"]/li/@data-url').extract()
        for package_url in package_urls:
            url = "https://packagist.org" + package_url
            # generate request to download package detail pages
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        parse the detail page
        """
        package = PackageItem()
        # html page of the response for later processing in case error occurs
        package['html'] = response.body
        package['vendor'] = response.url.split('/')[-2]
        package['name'] = response.url.split('/')[-1]
        package['tags'] = response.xpath('//p[@class="tags"]/a/text()').extract()

        # parse the downloads info
        package['downloads'] = {
            'overall': int(response.xpath('//p[@class="downloads"]/text()[2]').extract()[0].replace('installs', '').replace('install', '').replace(' ', '')),
            '30days': int(response.xpath('//p[@class="downloads"]/text()[4]').extract()[0].replace('installs', '').replace('install', '').replace(' ', '')),
            'today': int(response.xpath('//p[@class="downloads"]/text()[6]').extract()[0].replace('installs', '').replace('install', '').replace(' ', ''))
        }
        description = response.xpath('//p[@class="description"]/text()').extract()
        if description:
            package['description'] = description[0]

        # parse the details info
        package['details'] = {}
        details = response.xpath('//p[@class="details"]').extract()[0]
        details = details.replace('\n', '').replace('<p class="details">', '').replace('</p>', '').split('<br>')
        for d in details:
            d = Selector(text=d)
            # if the tag is span, i.e. the name of the detail info
            if d.xpath('//span/text()').extract():
                key = d.xpath('//span/text()').extract()[0].replace(':', '').lower()
                # when there is only one maintainer, the html tag is <span>Maintainer</span>
                # when there is more than one maintainer, the html tag is <span>Maintainers</span>
                # always use 'maintainers' as the key
                if key == 'maintainer':
                    key = 'maintainers'
                # list, one kind of detail can have multi values, each of which is in the form of {'url': '', 'content': ''}
                package['details'][key] = []
            # if the tag is a, i.e. the detail info
            # if the a tag has href attr and content, some <a> tags of details have no href or text
            if d.xpath('//a/@href').extract() and d.xpath('//a/text()').extract():
                detail = {
                    'url': d.xpath('//a/@href').extract()[0],
                    'content': d.xpath('//a/text()').extract()[0]
                }
                package['details'][key].append(detail)

        versions = response.xpath('//ul[@class="versions"]/li')
        # if there is at least one version
        if versions.extract():
            # parse the versions info, now only parse the latest version
            # TODO parse more versions
            package['versions'] = {}
            latest_version = {}
            latest_version['version'] = versions.xpath('section/h1/a/text()').extract()[0].replace('\n', '').replace(' ', '')
            latest_version['source-reference'] = versions.xpath('section/h1/span[@class="source-reference"]/text()').extract()[0].replace('reference: ', '')
            latest_version['release-date'] = versions.xpath('section/h1/span[@class="release-date"]/text()').extract()[0]
            licence = versions.xpath('section/h1/span[@class="license"]/text()').extract()
            if licence:
                latest_version['license'] = versions.xpath('section/h1/span[@class="license"]/text()').extract()[0]
            # TODO parse authors
            # requires, only parse packages that hold on packagist.org, i.e. those which have links
            # TODO parse packages which have no links
            latest_version['requires'] = []
            requires = versions.xpath('section//div[@class="requires"]/ul/li[a]')
            for r in requires:
                require = {
                    'vendor': r.xpath('a/@href').extract()[0].split('/')[2],
                    'name': r.xpath('a/@href').extract()[0].split('/')[3],
                    'version': r.xpath('./text()').extract()[0].replace(': ', '')
                }
                latest_version['requires'].append(require)
            # requires-dev, only parse packages that hold on packagist.org, i.e. those which have links
            # TODO parse packages which have no links
            latest_version['requires-dev'] = []
            requires_dev = versions.xpath('section//div[@class="devRequires"]/ul/li[a]')
            for r in requires_dev:
                require_dev = {
                    'vendor': r.xpath('a/@href').extract()[0].split('/')[2],
                    'name': r.xpath('a/@href').extract()[0].split('/')[3],
                    'version': r.xpath('./text()').extract()[0].replace(': ', '')
                }
                latest_version['requires-dev'].append(require_dev)
            # TODO parse suggests, provides conflicts and replaces

            package['versions']['latest'] = latest_version
        # yield PackageItem
        yield package