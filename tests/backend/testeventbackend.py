"""Test EventBackend."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from tests.tools.eventfactory import EventFactory
from backend.eventbackend import EventBackend
from support.messages.timestamp import TimeStamp


class TestEventBackend(object):

    """Test EventBaskend."""

    def test_init(self):
        """Test EventBackend.__init__(id)."""
        with DummyDB() as session:
            session.add(EventFactory())
            assert_equals(EventBackend(session, 1).id_, 1)

    def test_all(self):
        """Test EventBackend.all(session)."""
        with DummyDB() as session:
            session.add_all(EventFactory.build_batch(10))
            backends = EventBackend.all(session)
            assert_equals(len(backends), 10)

    def test_one(self):
        """Test EventBackend.one(session, subject, obj_id)."""
        with DummyDB() as session:
            EventFactory.reset_sequence()
            session.add(EventFactory())
            backend = EventBackend.one(session, "Test-event-0", 1)
            assert_equals(backend.id_, 1)

    def test_one_id(self):
        """Test EventBackend._one_id(session, id)."""
        with DummyDB() as session:
            event = EventFactory()
            session.add(event)
            # This is a test, we don't care about access protection.
            # pylint: disable=protected-access
            assert_equals(event, EventBackend._one_id(session, 1))

    def test_get(self):
        """Test EventBackend.get(session, key)."""
        with DummyDB() as session:
            session.add(EventFactory())
            backend = EventBackend(session, 1)
            assert_equals(backend.get(session, None, "time"), 0)

    def test_set(self):
        """Test EventBackend.set(session, key, value)."""
        with DummyDB() as session:
            session.add(EventFactory())
            backend = EventBackend(session, 1)
            backend.set(session, "time", 20)
            assert_equals(backend.get(session, None, "time"), 20)

    def test_update(self):
        """Test EventBackend.update(session, timestamp)."""
        with DummyDB() as session:
            session.add(EventFactory())
            backend = EventBackend(session, 1)
            backend.update(session, TimeStamp(1, 1))
            assert_equals(backend.get(session, None, "date"), 1)
            assert_equals(backend.get(session, None, "time"), 1)
