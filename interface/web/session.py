"""Thread safe session."""
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

SESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
