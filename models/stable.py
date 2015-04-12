import copy
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship, backref

from base import Base
from models.stableitem import StableItem
from support.messages.timestamp import TimeStamp


class Stable(Base):
    __tablename__ = 'stables'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    outside_surface = Column(Integer)
    light = Column(Integer)
    capacity = Column(Integer)

    cleanliness = Column(Float)
    cleanliness_date = Column(Integer)
    cleanliness_time = Column(Integer)

    items = relationship("StableItem", backref="stableitems")
    horses = relationship("Horse", backref="stable")

    def food(self):
        # from backend.time import time
        for item in self.items:
            if item.name == "food":
                item.value = 100
        # time.pass_time(5)

    def water(self):
        # from backend.time import time
        for item in self.items:
            if item.name == "water":
                item.value = 100
        # time.pass_time(5)

    def clean(self, now):
        # from backend.time import time
        # time.pass_time(15)

        # Cleaning the stable takes about 15 minutes
        now.add_min(15)

        # Regardless of current state, update cleanliness of stable.
        self.cleanliness = 100

        # Now update the next event time:
        e_info = self._ch_cleanliness(now)
        return {"clock": now, "e_info": e_info}

    def __repr__(self):
        return ''.join([
            "[",
            self.name,
            ", ",
            "surface: ",
            str(self.surface),
            ", ",
            "outside_surface: ",
            str(self.outside_surface),
            ", ",
            "light: ",
            str(self.light),
            ", ",
            "capacity: ",
            str(self.capacity),
            ", ",
            "cleanliness: ",
            str(self.cleanliness),
            ", ",
            "items: ",
            repr(self.items),
            ", ",
            "horses: ",
            repr(self.horses),
            "]"])

    def __str__(self):
        return ''.join([
                self.name,
                ": ",
                str([str(horse) for horse in self.horses])])

    def _get_limit(self, n):
        if n >= 76:
            return 75
        elif n >= 51:
            return 50
        elif n >= 26:
            return 25
        elif n >= 1:
            return 0
        else:
            return -1

    def _ch_cleanliness(self, now):
        last_updated = TimeStamp(self.cleanliness_date,
                                 self.cleanliness_time)
        time_passed = now - last_updated

        cleanliness_decay_time = 28
        if len(self.horses) > 0:
            self.cleanliness -= (time_passed.get_min() /
                                 float(cleanliness_decay_time))
            self.cleanliness_date = now.date
            self.cleanliness_time = now.time

        t_next = copy.copy(now)
        next_limit = self._get_limit(self.cleanliness)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "cleanliness", "t_stamp": t_next}

        t_next.add_min((self.cleanliness - next_limit) *
                       cleanliness_decay_time)
        return {"subject": "cleanliness", "t_stamp": t_next}

    def get(self, now, key):
        if key == "cleanliness":
            e_info = self._ch_cleanliness(now)
            result = self.cleanliness
        else:
            e_info = None
            result = getattr(self, key)
        return {"attr": result, "e_info": e_info}

    def get_events(self, now):
        events = []

        events.append(self._ch_cleanliness(now))

        return events

    def event(self, subject, t_stamp, night=False):
        if subject == "cleanliness":
            e_info = self._ch_cleanliness(t_stamp)

        return e_info
