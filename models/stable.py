from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref


class Stable(Base):
    __tablename__ = 'stables'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    outside_surface = Column(Integer)
    light = Column(Integer)
    capacity = Column(Integer)
    cleanliness = Column(Integer)
    items = relationship("StableItem", backref="stableitems")
    horses = relationship("Horse", backref="stable")

    def clean(self):
        self.cleanliness = 100

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
