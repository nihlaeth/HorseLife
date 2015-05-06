"""Stable model."""
import copy
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import relationship

from base import BASE
from support.messages.timestamp import TimeStamp


# Sqlalchemy takes care of __init__
# pylint: disable=no-init
class Stable(BASE):

    """Represents a stable."""

    __tablename__ = 'stables'

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    surface = Column(Integer)
    outside_surface = Column(Integer)
    light = Column(Integer)
    capacity = Column(Integer)

    cleanliness = Column(Float)
    cleanliness_date = Column(Integer)
    cleanliness_time = Column(Integer)
    cleanliness_msg = Column(Boolean)

    items = relationship("StableItem", backref="stableitems")
    horses = relationship("Horse", backref="stable")

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

    def clean(self, now):
        """Clean stable (takes about 15 minutes)."""
        # Cleaning the stable takes about 15 minutes
        now.add_min(15)

        # Regardless of current state, update cleanliness of stable.
        self.cleanliness = 100

        # Now update the next event time:
        e_info = self._ch_cleanliness(now)
        return {"clock": now, "e_info": e_info}

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

    def _ch_cleanliness(self, now):
        """Calculate current value of the cleanliness meter."""
        last_updated = TimeStamp(self.cleanliness_date,
                                 self.cleanliness_time)
        time_passed = now - last_updated

        cleanliness_decay_time = 28
        if len(self.horses) > 0:
            self.cleanliness -= (time_passed.get_min() /
                                 float(cleanliness_decay_time))
            self.cleanliness_date = now.date
            self.cleanliness_time = now.time

        if self.cleanliness <= 25 and not self.cleanliness_msg:
            msg = {
                "subject": "%s is getting dirty!" % self.__str__(),
                "t_stamp": now,
                "text": (
                    "Stables need regular cleaning, both for the health"
                    " of the horse(s) inside, and the integrity of the"
                    " building. Plus waste attracts vermin, and we don't"
                    " want that, do we? So go get your hands dirty and"
                    " clean that stable!")}
            self.cleanliness_msg = True
        else:
            msg = None
            if self.cleanliness > 25:
                self.cleanliness_msg = False

        t_next = copy.copy(now)
        next_limit = self._get_limit(self.cleanliness)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "cleanliness", "t_stamp": t_next, "msg": msg}

        t_next.add_min((self.cleanliness - next_limit) *
                       cleanliness_decay_time)
        return {"subject": "cleanliness", "t_stamp": t_next, "msg": msg}

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
