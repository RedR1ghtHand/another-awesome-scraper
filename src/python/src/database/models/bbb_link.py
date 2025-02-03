# -*- coding: utf-8 -*-
from sqlalchemy import Column, String


from src.python.src.database.models import Base
from .mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin


class BBBLink(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = 'bbb_links'

    url = Column('url', String(255), unique=True, nullable=False)
