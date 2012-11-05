"""
Initializes DB metadata.

"""

from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

DBSession = scoped_session(sessionmaker(extension = ZopeTransactionExtension()))
Base = declarative_base()
