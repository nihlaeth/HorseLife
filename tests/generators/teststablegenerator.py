from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from generators.stablegenerator import StableGenerator
from models.stable import Stable


class TestStableGenerator():
    def test_gen_one(self):
        print "Test StableGenerator._gen_one(location, b_type)"

        print "-- basic functionality"
        assert_equals(repr(StableGenerator()._gen_one("Shed")),
                      repr(Stable(
                               name="Shed",
                               surface = 9,
                               light = 0,
                               outside_surface = 0,
                               capacity = 1,
                               cleanliness = 100,
                               items = [],
                               horses = [])))


    def test_gen_many(self):
        print "Test StableGenerator.gen_many(session, n, b_type)"

        with DummyDB() as session:
            print "--test location increments"
            StableGenerator().gen_many(session, 3, "Shed")
            assert_equals(
                    session.query(Stable).count(),
                    3)

            StableGenerator().gen_many(session, 1, "Shed")
            assert_equals(
                    session.query(Stable).count(),
                    4)
