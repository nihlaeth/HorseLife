"""Message model."""
from base import BASE
from sqlalchemy import Column, String, Integer, Boolean

from support.messages.timestamp import TimeStamp


# pylint: disable=no-init
class Message(BASE):

    """Message model."""

    __tablename__ = 'messages'

    mid = Column(Integer, primary_key=True)

    subject = Column(String)
    date = Column(Integer)
    time = Column(Integer)
    text = Column(String)
    read = Column(Boolean)

    def get(self, _, key):
        """Get attribute."""
        return {"attr": getattr(self, key), "e_info": None}

    def get_time_stamp(self):
        """Return TimeStamp object."""
        return TimeStamp(self.date, self.time)

    def set(self, key, value):
        """Set attribute."""
        setattr(self, key, value)

    def __str__(self):
        """Message representation."""
        return " ".join([
            str(self.get_time_stamp()),
            "--",
            self.subject])
