from base import Base
from sqlalchemy import Column, Integer, String

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    age = Column(Integer)

