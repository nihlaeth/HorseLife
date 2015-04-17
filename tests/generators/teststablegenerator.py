from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from generators.stablegenerator import StableGenerator
from models.stable import Stable
from models.stableitem import StableItem
from support.messages.timestamp import TimeStamp


class TestStableGenerator():
    def test_gen_one(self):
        """ Test StableGenerator._gen_one(stable_type)"""
        assert_equals(repr(StableGenerator()._gen_one(
                            "Shed",
                            TimeStamp(0, 0))),
                      repr(Stable(
                               name="Shed",
                               surface=9,
                               light=0,
                               outside_surface=0,
                               capacity=1,
                               cleanliness=100,
                               cleanliness_date=0,
                               cleanliness_time=0,
                               items=[StableItem(name="food", value=0),
                                      StableItem(name="water", value=0)],
                               horses=[])))

    def test_gen_many(self):
        """ Test StableGenerator.gen_many(session, n, stable_type)"""
        with DummyDB() as session:
            StableGenerator().gen_many(session, 3, "Shed")
            assert_equals(
                    session.query(Stable).count(),
                    3)

            StableGenerator().gen_many(session, 1, "Shed")
            assert_equals(
                    session.query(Stable).count(),
                    4)
