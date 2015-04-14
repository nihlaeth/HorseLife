from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory
from backend.eventbackend import EventBackend
from support.messages.timestamp import TimeStamp


class TestEventBackend():
    def test_init(self):
        """ Test EventBackend.__init__(id)"""
        assert_equals(EventBackend(1)._id, 1)

    def test_all(self):
        """ Test EventBackend.all(session)"""
        with DummyDB() as session:
            session.add_all(EventFactory.build_batch(10))
            backends = EventBackend.all(session)
            assert_equals(len(backends), 10)

    def test_one(self):
        """ Test EventBackend.one(session, subject, obj_id)"""
        with DummyDB() as session:
            EventFactory.reset_sequence()
            session.add(EventFactory())
            backend = EventBackend.one(session, "Test-event-0", 1)

    def test_one_id(self):
        """ Test EventBackend._one_id(session, id)"""
        with DummyDB() as session:
            event = EventFactory()
            session.add(event)
            assert_equals(event, EventBackend._one_id(session, 1))

    def test_get(self):
        """ Test EventBackend.get(session, key)"""
        with DummyDB() as session:
            session.add(EventFactory())
            backend = EventBackend(1)
            assert_equals(backend.get(session, "time"), 0)

    def test_set(self):
        """ Test EventBackend.set(session, key, value)"""
        with DummyDB() as session:
            session.add(EventFactory())
            backend = EventBackend(1)
            backend.set(session, "time", 20)
            assert_equals(backend.get(session, "time"), 20)

    def test_update(self):
        """ Test EventBackend.update(session, timestamp)"""
        with DummyDB() as session:
            session.add(EventFactory())
            backend = EventBackend(1)
            backend.update(session, TimeStamp(1, 1))
            assert_equals(backend.get(session, "date"), 1)
            assert_equals(backend.get(session, "time"), 1)
