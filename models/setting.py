from base import Base
from sqlalchemy import Column, String, Integer


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    numeric = Column(Integer)
    text = Column(String)

    def get(self, now, key):
        return {"attr": getattr(self, key), "e_info": None}
