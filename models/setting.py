from base import Base
from sqlalchemy import Column, String, Integer


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(String)
