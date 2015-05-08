"""Empty database context manager to simplify testing."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import BASE
# These are not unused, they need to be here so BASE can create them in
# the database.
# pylint: disable=unused-import
from models.horse import Horse
from models.person import Person
from models.setting import Setting
from models.stable import Stable
from models.stableitem import StableItem
from models.message import Message
from models.story import Story
from models.transaction import Transaction
from models.pasture import Pasture


class DummyDB(object):

    """Provide a temporary, totally empty, database in RAM."""

    def __init__(self, debug=False):
        """Create database, BASE metadata and sessionfactory."""
        # Normally Session is not a valid name, but sessionmaker is
        # a generator, so it will actually house a class definition.
        # pylint: disable=invalid-name
        self._Session = sessionmaker()
        self._engine = create_engine('sqlite:///:memory:', echo=debug)
        self._Session.configure(bind=self._engine)
        BASE.metadata.create_all(self._engine)
        self._session = None

    def __enter__(self):
        """Return a fresh session."""
        self._session = self._Session()
        return self._session

    def __exit__(self, e_type, e_value, traceback):
        """Commit or rollback and cleanup."""
        if e_type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()
