from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from generators.settinggenerator import SettingGenerator
from backend.settingbackend import SettingBackend


class TestSettingGenerator():
    def test_gen_one(self):
        """ Test SettingGenerator._gen_one(name, numeric, text)"""
        setting = SettingGenerator._gen_one("test", 5, "some text")
        assert_equals(setting.name, "test")
        assert_equals(setting.numeric, 5)
        assert_equals(setting.text, "some text")

    def test_gen_many(self):
        """ Test SettingGenerator.gen_many(session, settings)"""
        with DummyDB() as session:
            settings = {
                    "setting1": [0, "blah"],
                    "setting2": [14, ""],
                    "setting3": [-5, "testing123"]}
            SettingGenerator.gen_many(session, settings)
            settings = SettingBackend.all(session)
            assert_equals(len(settings), 3)
