"""Setting model."""
from base import BASE
from sqlalchemy import Column, String, Integer


# Sqlalchemy takes care of __init__
# pylint: disable=no-init
class Setting(BASE):

    """Setting model."""

    __tablename__ = 'settings'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    numeric = Column(Integer)
    text = Column(String)

    def get(self, _, key):
        """Get attribute."""
        return {"attr": getattr(self, key), "e_info": None}
