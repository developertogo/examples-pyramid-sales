from sales.models import Base

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    Text,
    )
'''
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
'''

class SalesMonth(Base):
    __tablename__ = 'sales_month'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    created = Column(DateTime)

    def __init__(self, amount, created):
        self.amount = amount
        self.created = created
