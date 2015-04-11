from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, backref, reconstructor

from base import Base
from callback import Callback
from support.messages.timestamp import TimeStamp


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    date = Column(Integer)
    time = Column(Integer)
    night = Column(Boolean)
    t_stamp = None

    callbacks = relationship("Callback", backref="event")

    def __init__(self, date, time, subject, callbacks=[], night=False):
        self.subject = subject
        self.date = date
        self.time = time
        self.t_stamp = TimeStamp(date, time)
        self.callbacks = callbacks
        self.night = night

    @reconstructor
    def reconstruct(self):
        self.t_stamp = TimeStamp(self.date, self.time)

    def update(self, timestamp):
        self.t_stamp = timestamp
        self.date = timestamp.date
        self.time = timestamp.time

    def __str__(self):
        return ' '.join(["Event:",
                         self.subject,
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
