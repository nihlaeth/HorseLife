from base import Base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref


class StableItem(Base):
    __tablename__ = 'stableitems'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(Integer)
    stable_id = Column(Integer, ForeignKey('stables.id'))

    def __repr__(self):
        return ''.join([
            "[",
            self.name,
            ", ",
            str(self.value),
            "]"])
