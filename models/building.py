from base import Base
from sqlalchemy import Column, Integer, String

class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key = True)
    
    name = Column(String)
    building_type = Column(String)
    level = Column(Integer)
    location = Column(Integer)
