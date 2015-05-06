"""Person model."""
from base import BASE
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


# Sqlalchemy takes care of __init__
# pylint: disable=no-init
class Person(BASE):

    """Person model."""

    __tablename__ = 'people'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    age = Column(Integer)

    money = Column(Integer)

    horses = relationship("Horse", backref="owner")

    def spend_money(self, transaction):
        """Spend some of that hard earned money."""
        if self.money < transaction["amount"]:
            return False
        self.money -= transaction["amount"]
        # TODO create transaction
        return True

    def get(self, _, key):
        """Get attribute."""
        return {"attr": getattr(self, key), "e_info": None}

    def set(self, key, value):
        """Set attribute."""
        setattr(self, key, value)
