import scrapy

from rmq.items import RMQItem

class BBBLink(RMQItem):
    id = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
