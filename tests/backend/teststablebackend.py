from nose.tools import assert_equals, assert_less

from backend.stablebackend import StableBackend
from tests.tools.dummydb import DummyDB
from tests.tools.stablefactory import StableFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.stableitemfactory import StableItemFactory


class TestStableBackend():
    def test_all(self):
        print "Testing StableBackend.all(session)"
        with DummyDB() as session:
            stables = StableFactory.build_batch(3)
            session.add_all(stables)
            print "-- basic functionality"

            backends = StableBackend.all(session)
            assert_equals(backends[0]._id, 1)
            assert_equals(backends[2]._id, 3)

    def test_one_id(self):
        print "Testing StableBackend._one_id(session, id)"
        with DummyDB() as session:
            stables = StableFactory.build_batch(2)
            session.add_all(stables)
            stable = StableBackend._one_id(session, 1)
            assert_equals(stable.id, 1)
            stable = StableBackend._one_id(session, 2)
            assert_equals(stable.id, 2)

    def test_get(self):
        print "Testing StableBackend.get(session, name)"
        with DummyDB() as session:
            session.add(StableFactory.build(name="Test1"))
            backend = StableBackend(1)
            assert_equals(backend.get(session, "name"), "Test1")

    def test_set(self):
        print "Testing StableBackend.set(session, name, value)"
        with DummyDB() as session:
            session.add(StableFactory.build(name="Test1"))
            backend = StableBackend(1)
            assert_equals(backend.get(session, "name"), "Test1")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, "name"), "Test2")

    def test_pass_time(self):
        print "Test StableBackend.pass_time(session, minutes, night)"
        with DummyDB() as session:
            stable = StableFactory.build(
                    cleanliness=100,
                    horses=[HorseFactory.build()])
            session.add(stable)
            backend = StableBackend(1)
            backend.pass_time(session, 100, False)
            assert_less(backend.get(session, "cleanliness"), 100)

    def test_clean(self):
        print "Test StableBackend.clean(session)"
        with DummyDB() as session:
            stable = StableFactory(cleanliness=0)
            session.add(stable)
            backend = StableBackend(1)
            backend.clean(session)
            assert_equals(backend.get(session, "cleanliness"), 100)

    def test_food(self):
        print "Test StableBackend.food(session)"
        with DummyDB() as session:
            stable = StableFactory(items=[
                StableItemFactory(name="food", value=0)])
            session.add(stable)
            backend = StableBackend(1)
            backend.food(session)
            items = backend.get(session, "items")
            assert_equals(items[0].value, 100)

    def test_water(self):
        print "Test StableBackend.water(session)"
        with DummyDB() as session:
            stable = StableFactory(items=[
                StableItemFactory(name="water", value=0)])
            session.add(stable)
            backend = StableBackend(1)
            backend.water(session)
            items = backend.get(session, "items")
            assert_equals(items[0].value, 100)
