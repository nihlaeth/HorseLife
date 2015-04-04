from sqlalchemy import func
import ConfigParser

from generator import Generator
from models.stable import Stable
from models.stableitem import StableItem


class StableGenerator(Generator):
    def __init__(self):
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/stables.cfg")

    def _gen_one(self, stable_type):
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
                items=items,
                horses=[])

    def gen_many(self, session, n, stable_type):
        result = []
        for i in range(n):
            result.append(self._gen_one(stable_type))
        session.add_all(result)
        return result
