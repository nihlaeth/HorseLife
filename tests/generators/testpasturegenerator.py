"""Test PastureGenerator."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from generators.pasturegenerator import PastureGenerator
from models.pasture import Pasture
from support.messages.timestamp import TimeStamp


class TestPastureGenerator(object):

    """Test PastureGenerator."""

    def test_gen_one(self):
        """Test PastureGenerator._gen_one(pasture_type)."""
        # Testing a protected member
        # pylint: disable=protected-access
        assert_equals(
            repr(PastureGenerator()._gen_one(
                "Tiny Pasture",
                TimeStamp(0, 0))),
            repr(Pasture(
                name="Tiny Pasture",
                surface=16,
                capacity=1,
                cleanliness=100,
                cleanliness_date=0,
                cleanliness_time=0,
                cleanliness_msg=False,
                horses=[])))

    def test_gen_many(self):
        """Test PastureGenerator.gen_many(session, n, pasture_type)."""
        with DummyDB() as session:
            PastureGenerator().gen_many(session, 3, "Tiny Pasture")
            assert_equals(
                session.query(Pasture).count(),
                3)

            PastureGenerator().gen_many(session, 1, "Tiny Pasture")
            assert_equals(
                session.query(Pasture).count(),
                4)
