import scrapy

from rmq.utils import get_import_full_name
from pipelines import BBBMysqlLinkPipeline


class BBBSitemapSpider(scrapy.Spider):
    name = 'bbb_sitemap_spider'
    custom_settings = {
        "ITEM_PIPELINES": {get_import_full_name(BBBMysqlLinkPipeline): 300}
    }

    allowed_domains = ['bbb.org']
    start_urls = [
        'https://www.bbb.org/sitemap-accredited-business-profiles-index.xml',
        'https://www.bbb.org/sitemap-business-profiles-index.xml'
    ]

    def parse(self, response):
        response.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        indexes = response.xpath('//d:loc/text()').getall()
        for index in indexes:
            yield scrapy.Request(index, callback=self.parse_business)

    def parse_business(self, response):
        response.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        items = response.xpath('//d:loc/text()').getall()
        for item in items:
            yield {'url': item}
