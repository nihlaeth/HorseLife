from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, backref, reconstructor

from base import Base
from callback import Callback
from support.messages.timestamp import TimeStamp


class Event(Base):
    """ Represents an event in time, for instance, a horse getting hungry,
    or a stable getting dirty."""
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    obj_id = Column(Integer)
    date = Column(Integer)
    time = Column(Integer)
    t_stamp = None

    callbacks = relationship("Callback", backref="event")

    def __init__(self, date, time, subject, obj_id, callbacks=[]):
        """ Overwritten init so t_stamp is also initiated."""
        self.subject = subject
        self.obj_id = obj_id
        self.date = date
        self.time = time
        self.t_stamp = TimeStamp(date, time)
        self.callbacks = callbacks

    @reconstructor
    def reconstruct(self):
        """ Reconstruct t_stamp when sqlalchemy reconstructs this (__init__
        is skipped)."""
        self.t_stamp = TimeStamp(self.date, self.time)

    def update(self, timestamp):
        """ Update time and date information."""
        self.t_stamp = timestamp
        self.date = timestamp.date
        self.time = timestamp.time

    def __str__(self):
        return ' '.join(["Event:",
                         self.subject,
                         str(self.obj_id),
                         "Date:",
                         str(self.date),
                         "Time:",
                         str(self.time),
                         "Callbacks:",
                         str(self.callbacks),
                         "t_stamp:",
                         str(self.t_stamp)])

    def __eq__(self, other):
        if other is None:
            return False
        return self.t_stamp == other.t_stamp

    def __ne__(self, other):
        if other is None:
            return True
        return self.t_stamp != other.t_stamp

    def __lt__(self, other):
        if other is None:
            return False
        return self.t_stamp < other.t_stamp

    def __le__(self, other):
        if other is None:
            return False
        return self.t_stamp <= other.t_stamp

    def __gt__(self, other):
        if other is None:
            return False
        return self.t_stamp > other.t_stamp

    def __ge__(self, other):
        if other is None:
            return False
        return self.t_stamp >= other.t_stamp
