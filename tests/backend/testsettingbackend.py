from nose.tools import assert_equals

from backend.settingbackend import SettingBackend
from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from models.setting import Setting


class TestSettingBackend():
    def test_all(self):
        print "Testing SettingBackend.all(session)"
        with DummyDB() as session:
            settings = SettingFactory.build_batch(3)
            session.add_all(settings)
            print "-- basic functionality"

            backends = SettingBackend.all(session)
            assert_equals(backends[0]._id, 1)
            assert_equals(backends[2]._id, 3)

    def test_one(self):
        print "Testing SettingBackend.one(session, name)"
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            settings = SettingFactory.build_batch(3)
            session.add_all(settings)
            print "-- basic functionality"

            backend = SettingBackend.one(session, "Test0")
            assert_equals(backend._id, 1)
            backend = SettingBackend.one(session, "Test2")
            assert_equals(backend._id, 3)

    def test_one_id(self):
        print "Testing SettingBackend._one_id(session, id)"
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            settings = SettingFactory.build_batch(3)
            session.add_all(settings)
            setting = SettingBackend._one_id(session, 2)
            assert_equals(setting.name, "Test1")
            setting = SettingBackend._one_id(session, 3)
            assert_equals(setting.name, "Test2")

    def test_get(self):
        print "Testing SettingBackend.get(session, name)"
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            session.add(SettingFactory.build(numeric=34, text="blah"))
            backend = SettingBackend(1)
            assert_equals(backend.get(session, "name"), "Test0")
            assert_equals(backend.get(session, "numeric"), 34)
            assert_equals(backend.get(session, "text"), "blah")

    def test_set(self):
        print "Testing SettingBackend.set(session, name, value)"
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            session.add(SettingFactory.build())
            backend = SettingBackend(1)
            assert_equals(backend.get(session, "name"), "Test0")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, "name"), "Test2")
