import scrapy


class BBBScrapyItem(scrapy.Item):
    id = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    categories = scrapy.Field()
    full_address = scrapy.Field()
    website = scrapy.Field()
    image_url = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    bbb_rating = scrapy.Field()
    accredited_since = scrapy.Field()
    est_date = scrapy.Field()
    years_in_business = scrapy.Field()
    social_media = scrapy.Field()
    management = scrapy.Field()
    contacts = scrapy.Field()
