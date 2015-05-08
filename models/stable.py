"""Stable model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import BASE
from support.cleanlinessmixin import CleanlinessMixin
from support.messages.timestamp import TimeStamp


# Sqlalchemy takes care of __init__
# pylint: disable=no-init
class Stable(CleanlinessMixin, BASE):

    """Represents a stable."""

    __tablename__ = 'stables'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    outside_surface = Column(Integer)
    light = Column(Integer)
    capacity = Column(Integer)

    items = relationship("StableItem", backref="stableitems")
    horses = relationship("Horse", backref="stable")

    cleanliness_decay_time = 28
    cleaning_time = 15

    def food(self, now):
        """Fill the food tray in the stable."""
        for item in self.items:
            if item.name == "food":
                item.value = 100
        return {"clock": now.add_min(5)}

    def water(self, now):
        """Fill water tray in the stable."""
        for item in self.items:
            if item.name == "water":
                item.value = 100
        return {"clock": now.add_min(5)}

    def __repr__(self):
        """Return string representation of object."""
        return ''.join([
            "[",
            self.name,
            ", ",
            "surface: ",
            str(self.surface),
            ", ",
            "outside_surface: ",
            str(self.outside_surface),
            ", ",
            "light: ",
            str(self.light),
            ", ",
            "capacity: ",
            str(self.capacity),
            ", ",
            "cleanliness: ",
            str(self.cleanliness),
            ", ",
            "items: ",
            repr(self.items),
            ", ",
            "horses: ",
            repr(self.horses),
            "]"])

    def __str__(self):
        """Return string representation of object."""
        return ''.join([
            self.name,
            ": ",
            str([str(horse) for horse in self.horses])])

    def _get_limit(self, num):
        """Return next event boundary.

        Helper method for the _ch_* methods. It returns the next
        event boundary, dependent on current need value (n).
        """
        if num >= 26:
            return 25
        elif num >= 1:
            return 0
        else:
            return -1

    def _get_food(self, now):
        """Get up to date food value."""
        food = []
        for item in self.items:
            if item.name == "food":
                food.append(item)
        # For now, there's only one food item.
        # In the future, there will be different types here.
        # See if the horse wants to eat.
        events = []
        for horse in self.horses:
            result = horse.get(now, "food")
            if result["e_info"] is not None:
                events.append(result["e_info"][0])
        return {"attr": food[0].value, "e_info": events}

    def _get_water(self, now):
        """Get up to date water value."""
        water = []
        for item in self.items:
            if item.name == "water":
                water.append(item)
        # In the future, there will be multiple options here, horse
        # will have to choose from them somehow.
        # See if horse wants to drink.
        events = []
        for horse in self.horses:
            result = horse.get(now, "water")
            if result["e_info"] is not None:
                events.append(result["e_info"][0])
        return {"attr": water[0].value, "e_info": events}

    def get(self, now, key):
        """Get attribute.

        In case of an active attribute, calculate it's
        current value and return said value + info to update associated
        event.
        """
        if key == "cleanliness":
            last_checked = TimeStamp(
                self.cleanliness_date,
                self.cleanliness_time)
            if now == last_checked:
                e_info = None
            else:
                e_info = [self._ch_cleanliness(now)]
            result = self.cleanliness
        elif key == "food":
            data = self._get_food(now)
            e_info = data["e_info"]
            result = data["attr"]
        elif key == "water":
            data = self._get_water(now)
            e_info = data["e_info"]
            result = data["attr"]
        else:
            e_info = None
            result = getattr(self, key)
        return {"attr": result, "e_info": e_info}

    def get_events(self, now):
        """Get all the events needed for the operation of this object.

        Return the information necessary to construct them in the
        database.
        """
        events = []

        events.append(self._ch_cleanliness(now))

        return events

    def event(self, subject, t_stamp):
        """Execute event, gets called at event activation."""
        if subject == "cleanliness":
            e_info = self._ch_cleanliness(t_stamp)

        return e_info
