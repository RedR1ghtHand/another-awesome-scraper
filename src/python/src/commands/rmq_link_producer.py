from sqlalchemy.sql import select, update

from rmq.commands import Producer
from rmq.utils import TaskStatusCodes
from database.models import BBBLink


class RMQLinkProducer(Producer):
    """
    Example of calling this command:
    scrapy rmq_link_producer --chunk_size=100 --mode=worker
    """
    def __init__(self):
        super().__init__()
        self.task_queue_name = 'bbb_items_task_queue'
        self.reply_to_queue_name = 'bbb_task_reply_queue'

    def build_task_query_stmt(self, chunk_size):
        stmt = select([BBBLink]).where(
            BBBLink.status == TaskStatusCodes.NOT_PROCESSED.value
        ).order_by(BBBLink.id.asc()).limit(chunk_size)
        return stmt

    def build_message_body(self, db_task):
        return db_task

    def build_task_update_stmt(self, db_task, status):
        stmt = update(BBBLink).where(
            BBBLink.id == db_task['id']
        ).values(status=status)
        return stmt
