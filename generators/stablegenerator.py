from sqlalchemy import func
import ConfigParser

from support.messages.timestamp import TimeStamp
from generator import Generator
from models.stable import Stable
from models.stableitem import StableItem


class StableGenerator(Generator):
    def __init__(self):
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/stables.cfg")

    def _gen_one(self, stable_type, t_stamp):
        items = [StableItem(name="food", value=0),
                 StableItem(name="water", value=0)]
        return Stable(
                name=stable_type,
                surface=self._config.getint(stable_type, 'surface'),
                light=self._config.getint(stable_type, 'light'),
                outside_surface=self._config.getint(
                    stable_type,
                    'outside_surface'),
                capacity=self._config.getint(stable_type, 'capacity'),
                cleanliness=100,
                cleanliness_date=t_stamp.date,
                cleanliness_time=t_stamp.time,
                items=items,
                horses=[])

    def gen_many(self, session, n, stable_type, t_stamp=TimeStamp(0, 0)):
        result = []
        for i in range(n):
            result.append(self._gen_one(stable_type, t_stamp))
        session.add_all(result)
        session.flush()
        return result
