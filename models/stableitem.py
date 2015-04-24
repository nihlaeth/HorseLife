"""StableItem model."""
from base import BASE
from sqlalchemy import ForeignKey, Column, Integer, String


# Sqlalchemy takes care of __init__
# pylint: disable=no-init
class StableItem(BASE):

    """StableItem model."""

    __tablename__ = 'stableitems'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(Integer)
    stable_id = Column(Integer, ForeignKey('stables.mid'))

    def __repr__(self):
        """Return string representation of object."""
        return ''.join([
            "[",
            self.name,
            ", ",
            str(self.value),
            "]"])
