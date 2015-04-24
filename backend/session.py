"""Provide sqlalchemy sessions."""
from sqlalchemy.orm import sessionmaker

SESSION = sessionmaker()


# This is a content manager, it does not need any public methods.
# pylint: disable=too-few-public-methods
class SessionScope(object):

    """Content manager that creates sessions."""

    def __init__(self):
        """Create a session."""
        self._session = SESSION()

    def __enter__(self):
        """Return the session."""
        return self._session

    def __exit__(self, e_type, e_value, trace):
        """Commit or roll back, then do cleanup."""
        if e_type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()
