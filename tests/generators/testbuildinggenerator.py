from nose.tools import assert_equals
from sqlalchemy import func

from tests.tools.dummydb import DummyDB
from generators.buildinggenerator import BuildingGenerator
from models.building import Building
from models.buildingproperties import BuildingProperties


class TestBuildingGenerator():
    def test_gen_one(self):
        print "Test BuildingGenerator._gen_one(location, b_type)"

        print "-- basic functionality"
        assert_equals(repr(BuildingGenerator._gen_one(1, "Stable")),
                      repr(Building(
                               name="Stable",
                               building_type="Stable",
                               location=1,
                               properties=[BuildingProperties(
                                                name="Cleanliness",
                                                value=100)])))

    def test_gen_many(self):
        print "Test BuildingGenerator.gen_many(session, n, b_type)"

        with DummyDB() as session:
            print "--test location increments"
            BuildingGenerator.gen_many(session, 3)
            assert_equals(
                    session.query(func.max(Building.location)).scalar(),
                    2)

            BuildingGenerator.gen_many(session, 1)
            assert_equals(
                    session.query(func.max(Building.location)).scalar(),
                    3)
