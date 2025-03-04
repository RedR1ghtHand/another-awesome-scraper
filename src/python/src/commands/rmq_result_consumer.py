import json
from sqlalchemy.dialects.mysql import insert
from rmq.commands import Consumer
from database.models import BBBItem


class RMQResultConsumer(Consumer):
    """
    Example of calling this command:
    scrapy rmq_result_consumer --mode=worker
    """
    def __init__(self):
        super().__init__()
        self.queue_name = "spider_result_queue"

    def build_message_store_stmt(self, message_body):
        item_stmt = insert(BBBItem).values(
            url=message_body.get("url"),
            title=message_body.get("title"),
            categories=json.dumps(message_body.get("categories")),
            full_address=message_body.get("full_address"),
            website=message_body.get("website"),
            image_url=message_body.get("image_url"),
            phone=message_body.get("phone"),
            fax=message_body.get("fax"),
            bbb_rating=message_body.get("bbb_rating"),
            accredited_since=message_body.get("accredited_since"),
            est_date=message_body.get("est_date"),
            years_in_business=message_body.get("years_in_business"),
            social_media=json.dumps(message_body.get("social_media")),
            management=json.dumps(message_body.get("management")),
            contacts=json.dumps(message_body.get("contacts"))
        )

        return item_stmt
