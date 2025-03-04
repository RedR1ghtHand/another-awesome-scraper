import json
import scrapy
from scrapy.core.downloader.handlers.http11 import TunnelError

from rmq.spiders import TaskToMultipleResultsSpider
from rmq.utils import get_import_full_name
from rmq.utils.decorators import rmq_callback, rmq_errback
from rmq.pipelines import ItemProducerPipeline
from utils import extract_and_format_date
from items import BBBItem


class BBBTaskSpider(TaskToMultipleResultsSpider):
    """
    Example of calling this command:
    scrapy crawl bbb_task
    """
    name = 'bbb_task'
    custom_settings = {
        "ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, }
    }

    def __init__(self, *args, **kwargs):
        super(BBBTaskSpider, self).__init__(*args, **kwargs)
        self.task_queue_name = "bbb_items_task_queue"
        self.result_queue_name = "spider_result_queue"

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return scrapy.Request(
            url=data["url"],
            callback=self.parse,
            errback=self.errback,
            meta={"delivery_tag": _delivery_tag},
            dont_filter=True
        )

    @staticmethod
    def get_full_address(response):
        raw_address = response.xpath('//div[contains(@class, "bpr-overview-address")]//p/text()').getall()
        if raw_address:
            address = raw_address[0] + ', ' + "".join(raw_address[1:])
        # '23 Barnes Circle, Marlborough, MA 01752-4147'
            return address
        else:
            return ''

    @staticmethod
    def get_social_media_links(response):
        social_media_info = response.xpath('//dt[contains(text(), "Social Media")]/following-sibling::dd//a')
        social_media_links = {}

        for link in social_media_info:
            url = link.xpath('@href').get()
            platform = link.xpath('normalize-space()').get().strip().lower()
            social_media_links[f'{platform}'] = url

        return social_media_links

    @staticmethod
    def get_business_management(response):
        management_div = response.xpath("//div[contains(dt, 'Business Management')]/dd")
        management_list = []
        if management_div:
            for dd in management_div:
                manager = dd.xpath('text()').get()
                if len(manager.split(", ")) == 2:
                    name, position = manager.split(", ")
                    management_list.append({"name": name.strip(), "position": position.strip()})
                else:
                    name = manager
                    management_list.append({"name": name.strip(), "position": ''})

        return management_list

    @staticmethod
    def get_bbb_rating(response):
        rating = response.xpath("//div[@id='rating']/span/text()").get()
        if rating == 'Not Rated' or len(rating) > 2:
            rating = 'NR'

        return rating

    @staticmethod
    def get_accredited_since(response):
        raw_text = response.xpath("normalize-space(//p[contains(., 'BBB Accredited Since')])").get()
        return extract_and_format_date(raw_text)

    @staticmethod
    def get_establishment_date(response):
        raw_text = response.xpath("//dt[contains(text(), 'Business Started')]/following-sibling::dd/text()").get()
        return extract_and_format_date(raw_text)

    @staticmethod
    def get_additional_contact_info(response):
        data = {
            "Principal Contacts": [],
            "Fax numbers": [],
            "Additional Phone Numbers": []
        }

        additional_info_section = response.xpath('//div[h3[contains(text(), "Additional Contact Information")]]')

        for section in additional_info_section.xpath('.//div[contains(@class, "bpr-details-dl-data")]'):
            dt_text = section.xpath('./dt/text()').get(default="").strip()
            dd_elements = section.xpath('./dd')

            if dt_text == "Principal Contacts":
                for dd in dd_elements:
                    contact_text = dd.xpath('text()').get()
                    if contact_text and ", " in contact_text:
                        name, position = contact_text.split(", ", 1)
                        data["Principal Contacts"].append({"name": name.strip(), "position": position.strip()})
                    else:
                        data["Principal Contacts"].append({"name": contact_text.strip(), "position": ""})

            elif dt_text == "Fax numbers":
                data["Fax numbers"].extend([
                    dd.xpath('normalize-space(text()[last()])').get() for dd in dd_elements if
                    dd.xpath('text()').getall()
                ])

            elif dt_text == "Additional Phone Numbers":
                data["Additional Phone Numbers"].extend([
                    dd.xpath('normalize-space(./a/text()[last()])').get().strip() for dd in dd_elements
                    if dd.xpath('./a/text()').get()
                ])

        return data

    @rmq_callback
    def parse(self, response):
        item = BBBItem()
        item['url'] = response.url
        item['title'] = (response.xpath('//span[contains(@class, "business-name")]//text()').get()
                         or response.xpath('//p[contains(@class, "business-name")]//text()').get())
        item['categories'] = response.xpath(
            '//dt[contains(text(), "Business Categories")]/following-sibling::dd//a/text()').getall()
        item['full_address'] = self.get_full_address(response)
        item['website'] = response.xpath("//a[contains(text(), 'Website')]/@href").get()
        item['image_url'] = response.xpath("//img[contains(@class, 'logo')]/@src").get()
        item['phone'] = response.xpath("//a[contains(@href, 'tel')]/text()").get()
        item['fax'] = response.xpath("//div/dd[contains(text(), 'Fax')]/text()[last()]").get()
        item['bbb_rating'] = self.get_bbb_rating(response)
        item['accredited_since'] = self.get_accredited_since(response)
        item['est_date'] = self.get_establishment_date(response)
        item['years_in_business'] = response.xpath("//p[contains(., 'Years in Business')]//text()[2]").get()
        item['social_media'] = self.get_social_media_links(response)
        item['management'] = self.get_business_management(response)
        item['contacts'] = self.get_additional_contact_info(response)

        yield item

    @rmq_errback
    def errback(self, failure):
        if failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        else:
            self.logger.warning(f"IN ERRBACK: {repr(failure)}")
