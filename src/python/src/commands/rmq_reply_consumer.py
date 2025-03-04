from sqlalchemy.sql import update, ClauseElement

from rmq.commands import Consumer
from rmq.utils.sql_expressions import compile_expression
from database.models import BBBLink


class RMQReplyConsumer(Consumer):
    """
    Example of calling this command:
    scrapy rmq_reply_consumer --mode=worker
    """
    def __init__(self):
        super().__init__()
        self.queue_name = 'bbb_task_reply_queue'

    def process_message(self, transaction, message_body):
        stmt = (update(BBBLink)
                .where(BBBLink.id == message_body.get('id'))
                .values(status=message_body.get('status')))

        if isinstance(stmt, ClauseElement):
            transaction.execute(*compile_expression(stmt))
        else:
            transaction.execute(stmt)
        return True
