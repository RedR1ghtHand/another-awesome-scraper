import scrapy


class BBBLinkItem(scrapy.Item):
    id = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
