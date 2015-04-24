"""Callback model."""
from sqlalchemy import Column, Integer, String, ForeignKey

from base import BASE


# There's no init for a reason, sqlalchemy provides one that does
# everything we need already.
# pylint: disable=no-init
class Callback(BASE):

    """Callback model.

    Represents a weak callback, by providing an object name (str)
    and the id it will need to instanciate. It's meant to be used with
    Backend classes, though it's not necessarily restricted to that
    family.
    """

    __tablename__ = 'callbacks'
    mid = Column(Integer, primary_key=True)

    obj = Column(String)
    obj_id = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.mid'))

    def __repr__(self):
        """Return string representation of model."""
        return ''.join([
            self.obj,
            '-',
            str(self.obj_id)])
