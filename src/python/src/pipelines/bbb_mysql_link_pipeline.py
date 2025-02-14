from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from database.models import BBBLink
from utils import mysql_connection_string


class BBBMysqlLinkPipeline:
    def __init__(self, db_session):
        self.db_session = db_session

    @classmethod
    def from_crawler(cls, crawler):
        db_connection_string = mysql_connection_string()
        db_engine = create_engine(db_connection_string)
        db_session = sessionmaker(bind=db_engine)
        return cls(db_session)

    def open_spider(self, spider):
        self.session = self.db_session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        business_url = item.get('url')
        # business_url = f"{item.get('url')}/details"
        if business_url:
            try:
                query = insert(BBBLink.__table__).values(url=business_url)
                self.session.execute(query)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                spider.logger.error("Database insertion error: %s", str(e))
        return item
