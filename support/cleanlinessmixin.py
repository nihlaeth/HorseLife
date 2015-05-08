"""Mixin class that provides cleanliness attribute for models."""
import copy
from sqlalchemy import Column, Integer, Float, Boolean

from messages.timestamp import TimeStamp


class CleanlinessMixin(object):

    """Provide cleanliness attribute for models."""

    cleanliness = Column(Float)
    cleanliness_date = Column(Integer)
    cleanliness_time = Column(Integer)
    cleanliness_msg = Column(Boolean)

    def _ch_cleanliness(self, now):
        """Calculate current value of the cleanliness meter."""
        last_updated = TimeStamp(self.cleanliness_date,
                                 self.cleanliness_time)
        time_passed = now - last_updated

        if len(self.horses) > 0:
            self.cleanliness -= (time_passed.get_min() /
                                 float(self.cleanliness_decay_time))
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
                       self.cleanliness_decay_time)
        return {"subject": "cleanliness", "t_stamp": t_next, "msg": msg}

    def clean(self, now):
        """Clean stable (takes about 15 minutes)."""
        # Cleaning the stable takes about 15 minutes
        now.add_min(self.cleaning_time)

        # Regardless of current state, update cleanliness of stable.
        self.cleanliness = 100

        # Now update the next event time:
        e_info = self._ch_cleanliness(now)
        return {"clock": now, "e_info": e_info}
