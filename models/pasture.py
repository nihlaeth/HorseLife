"""Pasture model."""
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from base import BASE


# pylint: disable=no-init
class Pasture(BASE):

    """Pasture (and paddock) model."""

    __tablename__ = 'pastures'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    food = Column(Boolean)
    capacity = Column(Integer)

    cleanliness = Column(Float)
    cleanliness_date = Column(Integer)
    cleanliness_time = Column(Integer)
    cleanliness_msg = Column(Boolean)

    horses = relationship("Horse", backref="pasture")
