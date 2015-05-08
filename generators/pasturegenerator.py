"""Generator for Pasture models."""
import ConfigParser

from support.messages.timestamp import TimeStamp
from generator import Generator
from models.pasture import Pasture


class PastureGenerator(Generator):

    """Generator for Pasture models."""

    def __init__(self):
        """Set up config parser."""
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/pastures.cfg")

    # Arguments are supposed to be different from parent class method.
    # pylint: disable=arguments-differ
    def _gen_one(self, pasture_type, t_stamp):
        """Generate a single Pasture model.

        pasture_type -- type of pasture / config section
        t_stamp -- TimeStamp at which this pasture is created
        --> important for event generation
        """
        return Pasture(
            name=pasture_type,
            surface=self._config.getint(pasture_type, 'surface'),
            capacity=self._config.getint(pasture_type, 'capacity'),
            food=self._config.getboolean(pasture_type, "food"),
            cleanliness=100,
            cleanliness_date=t_stamp.date,
            cleanliness_time=t_stamp.time,
            cleanliness_msg=False,
            horses=[])

    def gen_many(self, session, num, pasture_type, t_stamp=TimeStamp(0, 0)):
        """Generate one or more Pasture models and add them to the session.

        session -- sqlalchemy session
        num -- number of Pasture models to create
        pasture_type -- pasture type / config section
        t_stamp -- TimeStamp object indicating model creation time
        --> important for event generation.
        """
        result = []
        for _ in range(num):
            result.append(self._gen_one(pasture_type, t_stamp))
        session.add_all(result)
        session.flush()
        return result
