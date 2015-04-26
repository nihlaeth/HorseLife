"""Test HorseGenerator."""
from nose.tools import assert_equals

from support.messages.timestamp import TimeStamp
from tests.tools.dummydb import DummyDB
from generators.horsegenerator import HorseGenerator
from backend.horsebackend import HorseBackend


class TestHorseGenerator(object):

    """Test HorseGenerator."""

    def test_gen_one(self):
        """Test HorseGenerator._gen_one(breed, t_stamp, training)."""
        # We're testing a protected member.
        # pylint: disable=protected-access
        horse = HorseGenerator()._gen_one("random", TimeStamp(0, 0))
        assert_equals(horse.name, "Nameless")

    def test_gen_many(self):
        """Test HorseGenerator.gen_many(session, n, breed, t_stamp)."""
        with DummyDB() as session:
            HorseGenerator().gen_many(session, 20)
            horses = HorseBackend.all(session)
            assert_equals(len(horses), 20)
