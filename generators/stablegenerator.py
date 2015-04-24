"""Generator for Stable models."""
import ConfigParser

from support.messages.timestamp import TimeStamp
from generator import Generator
from models.stable import Stable
from models.stableitem import StableItem


class StableGenerator(Generator):

    """Generator for Stable models."""

    def __init__(self):
        """Set up config parser."""
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/stables.cfg")

    # Arguments are supposed to be different from parent class method.
    # pylint: disable=arguments-differ
    def _gen_one(self, stable_type, t_stamp):
        """Generate a single Stable model.

        stable_type -- type of stable / config section
        t_stamp -- TimeStamp at which this stable is created
        --> important for event generation
        """
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

    def gen_many(self, session, num, stable_type, t_stamp=TimeStamp(0, 0)):
        """Generate one or more Stable models and add them to the session.

        session -- sqlalchemy session
        num -- number of Stable models to create
        stable_type -- stable type / config section
        t_stamp -- TimeStamp object indicating model creation time
        --> important for event generation.
        """
        result = []
        for _ in range(num):
            result.append(self._gen_one(stable_type, t_stamp))
        session.add_all(result)
        session.flush()
        return result
