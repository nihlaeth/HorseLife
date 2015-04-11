from sqlalchemy import Column, Integer, String, ForeignKey

from base import Base


class Callback(Base):
    __tablename__ = 'callbacks'
    id = Column(Integer, primary_key=True)

    obj = Column(String)
    obj_id = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'))

    def __repr__(self):
        return ''.join([
            self.obj,
            '-',
            str(self.obj_id)])
