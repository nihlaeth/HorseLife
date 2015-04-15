import mock
from nose.tools import assert_equals, assert_less, assert_greater

from backend.stablebackend import StableBackend
from backend.eventbackend import EventBackend
from models.stable import Stable
from support.messages.timestamp import TimeStamp
from tests.tools.dummydb import DummyDB
from tests.tools.stablefactory import StableFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.stableitemfactory import StableItemFactory
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory


class TestStableBackend():
    def test_all_raw(self):
        """ Test StanleBackend.all_raw(session)"""
        with DummyDB() as session:
            session.add_all(StableFactory.build_batch(20))
            assert_equals(StableBackend.all_raw(session).count(), 20)

    def test_all(self):
        """ Test StableBackend.all(session)"""
        with DummyDB() as session:
            stables = StableFactory.build_batch(3)
            session.add_all(stables)
            backends = StableBackend.all(session)
            assert_equals(backends[0]._id, 1)
            assert_equals(backends[2]._id, 3)

    def test_one_id(self):
        """ Test StableBackend._one_id(session, id)"""
        with DummyDB() as session:
            stables = StableFactory.build_batch(2)
            session.add_all(stables)
            stable = StableBackend._one_id(session, 1)
            assert_equals(stable.id, 1)
            stable = StableBackend._one_id(session, 2)
            assert_equals(stable.id, 2)

    def test_get(self):
        """ Test StableBackend.get(session, timestamp, key)"""
        with DummyDB() as session:
            session.add(StableFactory.build(name="Test1",
                        horses=[HorseFactory()]))
            backend = StableBackend(1)
            backend.get_events(session, TimeStamp(0, 0))
            assert_equals(backend.get(session, None, "name"), "Test1")
            # Now see if cleanliness behaves as it should.
            t1 = TimeStamp(0, 0)
            t2 = TimeStamp(0, 120)
            assert_equals(backend.get(session, t1, "cleanliness"), 100)
            assert_less(backend.get(session, t2, "cleanliness"), 100)

    def test_set(self):
        """ Test StableBackend.set(session, key, value)"""
        with DummyDB() as session:
            session.add(StableFactory.build(name="Test1"))
            backend = StableBackend(1)
            assert_equals(backend.get(session, None, "name"), "Test1")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, None, "name"), "Test2")

    def test_clean(self):
        """ Test StableBackend.clean(session, timestamp)"""
        with DummyDB() as session:
            session.add_all([
                StableFactory(cleanliness=0)])
            backend = StableBackend(1)
            backend.get_events(session, TimeStamp(0, 0))
            t_stamp = backend.clean(session, TimeStamp(0, 0))
            assert_equals(t_stamp.time, 15)
            assert_equals(backend.get(
                session,
                t_stamp,
                "cleanliness"), 100)

    def test_food(self):
        """ Test StableBackend.food(session)"""
        with DummyDB() as session:
            stable = StableFactory(items=[
                StableItemFactory(name="food", value=0)])
            session.add(stable)
            backend = StableBackend(1)
            backend.food(session)
            items = backend.get(session, None, "items")
            assert_equals(items[0].value, 100)

    def test_water(self):
        """ Test StableBackend.water(session)"""
        with DummyDB() as session:
            stable = StableFactory(items=[
                StableItemFactory(name="water", value=0)])
            session.add(stable)
            backend = StableBackend(1)
            backend.water(session)
            items = backend.get(session, None, "items")
            assert_equals(items[0].value, 100)

    def test_get_events(self):
        """ Test StableBackend.get_events(session, timestamp)"""
        with DummyDB() as session:
            session.add(StableFactory())
            backend = StableBackend(1)
            backend.get_events(session, TimeStamp(0, 0))
            assert_greater(len(EventBackend.all(session)), 0)

    def test_update_event(self):
        """ Test StableBackend._update_event(session, e_info)"""
        with DummyDB() as session:
            session.add_all([
                StableFactory(),
                EventFactory(subject="flub")])
            backend = StableBackend(1)

            backend._update_event(session, {
                "subject": "flub",
                "t_stamp": TimeStamp(5, 20)})

            event = EventBackend(1)
            assert_equals(event.get(session, "date"), 5)
            assert_equals(event.get(session, "time"), 20)

    def test_event_callback(self):
        """ Test StableBackend.event_callback(session, subject, timestamp)"""
        with DummyDB() as session:
            session.add_all([
                StableFactory(),
                EventFactory(subject="stablestest",
                             callbacks=[CallbackFactory(
                                 obj="StableBackend",
                                 obj_id=1)])])
            with mock.patch.object(Stable, "event") as m:
                m.return_value = {
                        "subject": "stablestest",
                        "t_stamp": TimeStamp(1000, 0)}
                backend = StableBackend(1)
                t_stamp = TimeStamp(0, 0)
                backend.event_callback(session, "stablestest", t_stamp)

                m.assert_called_once_with("stablestest", t_stamp)
        # Now test it without the mock!
        with DummyDB() as session:
            session.add_all([
                StableFactory()])
            backend = StableBackend(1)
            backend.get_events(session, TimeStamp(0, 0))
            t_stamp = TimeStamp(0, 0)
            backend.event_callback(session, "cleanliness", t_stamp)
            event = EventBackend.one(session, "cleanliness", 1)
            assert_greater(event.get(session, "time"), 0)
