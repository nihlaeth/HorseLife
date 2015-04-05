from nose.tools import assert_equals

from backend.settingsbackend import SettingsBackend
from tests.tools.dummydb import DummyDB
from models.setting import Setting


class TestSettingsBackend():
    def test_all(self):
        print "Testing SettingsBackend.all(session)"
        with DummyDB() as session:
            settings = [Setting(name="Test1", numeric=20, text=""),
                        Setting(name="Test2", numeric=15, text=""),
                        Setting(name="Test3", numeric=33, text="hey")]
            session.add_all(settings)
            print "-- basic functionality"

            backends = SettingsBackend.all(session)
            assert_equals(backends[0]._id, 1)
            assert_equals(backends[2]._id, 3)

    def test_one(self):
        print "Testing SettingsBackend.one(session, name)"
        with DummyDB() as session:
            settings = [Setting(name="Test1", numeric=11, text=""),
                        Setting(name="Test2", numeric=13, text="bye")]
            session.add_all(settings)
            print "-- basic functionality"

            backend = SettingsBackend.one(session, "Test1")
            assert_equals(backend._id, 1)
            backend = SettingsBackend.one(session, "Test2")
            assert_equals(backend._id, 2)

    def test_one_id(self):
        print "Testing SettingsBackend._one_id(session, id)"
        with DummyDB() as session:
            settings = [Setting(name="Test1", numeric=42, text="b"),
                        Setting(name="Test2", numeric=12, text="")]
            session.add_all(settings)
            setting = SettingsBackend._one_id(session, 1)
            assert_equals(setting.name, "Test1")
            setting = SettingsBackend._one_id(session, 2)
            assert_equals(setting.name, "Test2")

    def test_get(self):
        print "Testing SettingsBackend.get(session, name)"
        with DummyDB() as session:
            session.add(Setting(name="Test1", numeric=34, text="blah"))
            backend = SettingsBackend(1)
            assert_equals(backend.get(session, "name"), "Test1")
            assert_equals(backend.get(session, "numeric"), 34)
            assert_equals(backend.get(session, "text"), "blah")

    def test_set(self):
        print "Testing SettingsBackend.set(session, name, value)"
        with DummyDB() as session:
            session.add(Setting(name="Test1", numeric=22, text="duhh"))
            backend = SettingsBackend(1)
            assert_equals(backend.get(session, "name"), "Test1")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, "name"), "Test2")
