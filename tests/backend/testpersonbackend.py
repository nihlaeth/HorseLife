"""Test PersonBackend."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from tests.tools.personfactory import PersonFactory
from backend.personbackend import PersonBackend


class TestPersonBackend(object):

    """Test PersonBackend."""

    def test_init(self):
        """Test PersonBackend.__init__(id)."""
        backend = PersonBackend(1)
        assert_equals(backend.id_, 1)

    def test_one_id(self):
        """Test PersonBackend._one_id(session, id)."""
        with DummyDB() as session:
            person = PersonFactory()
            session.add(person)
            # The whole point here is to test a protected method.
            # pylint: disable=protected-access
            assert_equals(PersonBackend._one_id(session, 1), person)

    def test_one(self):
        """Test PersonBackend.one(session, name)."""
        with DummyDB() as session:
            PersonFactory.reset_sequence()
            session.add(PersonFactory())
            backend = PersonBackend.one(session, "Test0")
            assert_equals(backend.id_, 1)

    def test_all(self):
        """Test PersonBackend.all(session)."""
        with DummyDB() as session:
            session.add_all(PersonFactory.build_batch(20))
            backends = PersonBackend.all(session)
            assert_equals(len(backends), 20)
