"""Test MessageBackend."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from tests.tools.messagefactory import MessageFactory
from backend.messagebackend import MessageBackend


class TestMessageBackend(object):

    """Test MessageBackend."""

    def test_all(self):
        """Test MessageBackend.all(session)."""
        with DummyDB() as session:
            session.add_all(MessageFactory.build_batch(20))
            messages = MessageBackend.all(session)
            assert_equals(len(messages), 20)

    def test_one(self):
        """Test MessageBackend.one(session, id)."""
        with DummyDB() as session:
            session.add(MessageFactory())
            backend = MessageBackend.one(session, 1)
            assert_equals(backend.id_, 1)

    def test_one_id(self):
        """Test MessageBackend._one_id(session, id)."""
        with DummyDB() as session:
            message = MessageFactory()
            session.add(message)
            # pylint: disable=protected-access
            assert_equals(MessageBackend._one_id(session, 1), message)

    def test_init(self):
        """Test MessageBackend.__init__(id)."""
        assert_equals(MessageBackend(1).id_, 1)

    def test_set(self):
        """Test MessageBackend.set(session, key, value)."""
        with DummyDB() as session:
            session.add(MessageFactory())
            backend = MessageBackend(1)
            backend.set(session, "date", 20)
            assert_equals(backend.get(session, None, "date"), 20)

    def test_get(self):
        """Test MessageBackend.get(session, t_stamp, key)."""
        with DummyDB() as session:
            session.add(MessageFactory())
            backend = MessageBackend(1)
            assert_equals(backend.get(session, None, "subject"), "Hey")
            assert_equals(backend.get(session, None, "read"), False)
