from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship, backref

from base import Base
from models.stableitem import StableItem


class Stable(Base):
    __tablename__ = 'stables'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    outside_surface = Column(Integer)
    light = Column(Integer)
    capacity = Column(Integer)
    cleanliness = Column(Float)
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

    def clean(self):
        # from backend.time import time
        # time.pass_time(15)
        self.cleanliness = 100

    def pass_time(self, minutes, night):
        if len(self.horses) > 0:
            # Decay no matter if the horse(s) is/are actually in
            # the stable. It's needlessly complicated to account
            # for their whereabouts, and a stable needs to be mucked
            # out every day anyway.
            minutes_per_decay = 28
            self.cleanliness -= minutes / minutes_per_decay

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
