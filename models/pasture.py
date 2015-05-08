"""Pasture model."""
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from base import BASE
from support.cleanlinessmixin import CleanlinessMixin
from support.messages.timestamp import TimeStamp


# pylint: disable=no-init
class Pasture(CleanlinessMixin, BASE):

    """Pasture (and paddock) model."""

    __tablename__ = "pastures"

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    capacity = Column(Integer)
    food = Column(Boolean)

    horses = relationship("Horse", backref="pasture")

    cleanliness_decay_time = 120
    cleaning_time = 60

    def _get_limit(self, num):
        """Return next event boundary."""
        if num >= 26:
            return 25
        elif num >= 1:
            return 0
        else:
            return -1

    def get(self, now, key):
        """Get attribute."""
        if key == "cleanliness":
            last_checked = TimeStamp(
                self.cleanliness_date,
                self.cleanliness_time)
            if now == last_checked:
                e_info = None
            else:
                e_info = [self._ch_cleanliness(now)]
            result = self.cleanliness
        else:
            e_info = None
            result = getattr(self, key)
        return {"attr": result, "e_info": e_info}

    def event(self, subject, t_stamp):
        """Execute event."""
        if subject == "cleanliness":
            e_info = self._ch_cleanliness(t_stamp)

        return e_info

    def get_events(self, now):
        """Get all the events needed for pasture to operate."""
        events = []

        events.append(self._ch_cleanliness(now))

        return events

    def __repr__(self):
        """Return string representation."""
        return " ".join([
            self.name,
            "Surface:",
            str(self.surface),
            "Capacity:",
            str(self.capacity),
            "Cleanliness:",
            str(self.cleanliness),
            "Cleanliness date:",
            str(self.cleanliness_date),
            "Cleanliness time:",
            str(self.cleanliness_time),
            "Cleanliness msg:",
            str(self.cleanliness_msg),
            "Horses:",
            str(self.horses)])
