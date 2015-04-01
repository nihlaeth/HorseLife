from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref


class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    building_type = Column(String)
    location = Column(Integer)

    properties = relationship(
            "BuildingProperties",
            order_by="BuildingProperties.id",
            backref="buildings")

    def __repr__(self):
        return ''.join([
            "[",
            self.name,
            ", ",
            self.building_type,
            ", ",
            str(self.location),
            ", ",
            repr(self.properties),
            "]"])

    def __str__(self):
        return ''.join(["#", str(self.location), " ", self.name])
