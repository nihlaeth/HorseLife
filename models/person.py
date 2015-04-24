"""Person model."""
from base import BASE
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


# Sqlalchemy takes care of __init__
# pylint: disable=no-init
class Person(BASE):

    """Person model."""

    __tablename__ = 'people'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    age = Column(Integer)

    money = Column(Integer)

    horses = relationship("Horse", backref="owner")
