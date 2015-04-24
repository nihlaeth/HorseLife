from nose.tools import assert_equals

from backend.settingbackend import SettingBackend
from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from models.setting import Setting


class TestSettingBackend():
    def test_all(self):
        """ Test SettingBackend.all(session)"""
        with DummyDB() as session:
            settings = SettingFactory.build_batch(3)
            session.add_all(settings)
            backends = SettingBackend.all(session)
            assert_equals(backends[0].id_, 1)
            assert_equals(backends[2].id_, 3)

    def test_one(self):
        """ Test SettingBackend.one(session, name)"""
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            settings = SettingFactory.build_batch(3)
            session.add_all(settings)
            backend = SettingBackend.one(session, "Test0")
            assert_equals(backend.id_, 1)
            backend = SettingBackend.one(session, "Test2")
            assert_equals(backend.id_, 3)

    def test_one_id(self):
        """ Test SettingBackend._one_id(session, id)"""
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            settings = SettingFactory.build_batch(3)
            session.add_all(settings)
            setting = SettingBackend._one_id(session, 2)
            assert_equals(setting.name, "Test1")
            setting = SettingBackend._one_id(session, 3)
            assert_equals(setting.name, "Test2")

    def test_get(self):
        """ Test SettingBackend.get(session, key)"""
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            session.add(SettingFactory.build(numeric=34, text="blah"))
            backend = SettingBackend(1)
            assert_equals(backend.get(session, None, "name"), "Test0")
            assert_equals(backend.get(session, None, "numeric"), 34)
            assert_equals(backend.get(session, None, "text"), "blah")

    def test_set(self):
        """ Test SettingBackend.set(session, key, value)"""
        with DummyDB() as session:
            SettingFactory.reset_sequence()
            session.add(SettingFactory.build())
            backend = SettingBackend(1)
            assert_equals(backend.get(session, None, "name"), "Test0")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, None, "name"), "Test2")
