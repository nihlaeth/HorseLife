from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    age = Column(Integer)

    money = Column(Integer)

    horses = relationship("Horse", backref="owner")
