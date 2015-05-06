"""Person model."""
from base import BASE
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.transaction import Transaction


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
    transactions = relationship("Transaction", backref="person")

    def spend_money(self, transaction):
        """Spend some of that hard earned money."""
        if self.money < transaction["amount"]:
            return False
        self.money -= transaction["amount"]
        self.transactions.append(Transaction(
            subject=transaction["subject"],
            date=transaction["t_stamp"].date,
            time=transaction["t_stamp"].time,
            amount=int(transaction["amount"])))
        return True

    def get(self, _, key):
        """Get attribute."""
        return {"attr": getattr(self, key), "e_info": None}

    def set(self, key, value):
        """Set attribute."""
        setattr(self, key, value)
