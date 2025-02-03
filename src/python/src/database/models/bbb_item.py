# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL

from src.python.src.database.models import Base
from .mixins import MysqlTimestampsMixin, MysqlPrimaryKeyMixin


class BBBItem(Base, MysqlTimestampsMixin, MysqlPrimaryKeyMixin):
    __tablename__ = 'bbb_items'

    url = Column('url', String(255), unique=True, nullable=False)
    title = Column('title', String(255), nullable=False)
    categories = Column('categories', JSON)
    full_address = Column('full_address', String(255))
    website = Column('website', String(255))
    image_url = Column('image_url', String(255))
    phone = Column('phone', String(20))
    fax = Column('fax', String(20))
    hours_of_operation = Column('hours_of_operation', JSON)
    bbb_rating = Column('bbb_rating', String(2))
    accredited_since = Column('accredited_since', Date)
    est_date = Column('est_date', Date)
    years_in_business = Column('years_in_business', Integer)
    social_media = Column('social_media', JSON)
    management = Column('management', JSON)
    contacts = Column('contacts', JSON)
