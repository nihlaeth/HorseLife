"""Transaction model."""
from base import BASE
from sqlalchemy import ForeignKey, Column, Integer, String

from support.messages.timestamp import TimeStamp


# pylint: disable=no-init
class Transaction(BASE):

    """Transaction model."""

    __tablename__ = 'transactions'

    mid = Column(Integer, primary_key=True)

    subject = Column(String)
    date = Column(Integer)
    time = Column(Integer)
    amount = Column(Integer)

    person_id = Column(Integer, ForeignKey('people.mid'))

    def __str__(self):
        """Return string representation."""
        return " ".join([
            self.subject,
            "--",
            str(TimeStamp(self.date, self.time)),
            "--",
            "$",
            str(self.amount)])
