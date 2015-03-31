from base import Base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref


class BuildingProperties(Base):
    __tablename__ = 'buildingproperties'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(Integer)
    building_id = Column(Integer, ForeignKey('buildings.id'))

    building = relationship("Building",
                            backref=backref('buildings', order_by=id))
