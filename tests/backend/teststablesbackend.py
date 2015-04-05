from nose.tools import assert_equals

from backend.stablesbackend import StablesBackend
from tests.tools.dummydb import DummyDB
from models.stable import Stable


class TestStablesBackend():
    def test_all(self):
        print "Testing StablesBackend.all(session)"
        with DummyDB() as session:
            stables = [Stable(name="Test1"),
                       Stable(name="Test2"),
                       Stable(name="Test3")]
            session.add_all(stables)
            print "-- basic functionality"

            backends = StablesBackend.all(session)
            assert_equals(backends[0]._id, 1)
            assert_equals(backends[2]._id, 3)

    def test_one(self):
        print "Testing StablesBackend.one(session, name)"
        with DummyDB() as session:
            stables = [Stable(name="Test1"),
                       Stable(name="Test2")]
            session.add_all(stables)
            print "-- basic functionality"
            # This test is a bit idiotic, since we only fetch
            # stables by id. But I guess it'll expose bugs
            # nonetheless.
            backend = StablesBackend.one(session, 1)
            assert_equals(backend._id, 1)
            backend = StablesBackend.one(session, 2)
            assert_equals(backend._id, 2)

    def test_one_id(self):
        print "Testing StablesBackend._one_id(session, id)"
        with DummyDB() as session:
            stables = [Stable(name="Test1"),
                       Stable(name="Test2")]
            session.add_all(stables)
            stable = StablesBackend._one_id(session, 1)
            assert_equals(stable.name, "Test1")
            stable = StablesBackend._one_id(session, 2)
            assert_equals(stable.name, "Test2")

    def test_get(self):
        print "Testing StablesBackend.get(session, name)"
        with DummyDB() as session:
            session.add(Stable(name="Test1"))
            backend = StablesBackend(1)
            assert_equals(backend.get(session, "name"), "Test1")

    def test_set(self):
        print "Testing StablesBackend.set(session, name, value)"
        with DummyDB() as session:
            session.add(Stable(name="Test1"))
            backend = StablesBackend(1)
            assert_equals(backend.get(session, "name"), "Test1")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, "name"), "Test2")
