from nose.tools import assert_equals, assert_less, assert_greater

from backend.horsebackend import HorseBackend
from backend.time import time
from tests.tools.dummydb import DummyDB
from tests.tools.horsefactory import HorseFactory
from tests.tools.settingfactory import SettingFactory


class TestHorseBackend():
    def test_init(self):
        assert_equals(HorseBackend(1)._id, 1)

    def test_one_id(self):
        with DummyDB() as session:
            session.add(HorseFactory.build())
            assert_equals(HorseBackend._one_id(session, 1).id, 1)

    def test_all(self):
        with DummyDB() as session:
            horses = HorseFactory.build_batch(10)
            session.add_all(horses)
            backends = HorseBackend.all(session)
            assert_equals(len(backends), 10)

    def test_get(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Spirit"))
            backend = HorseBackend(1)
            assert_equals(backend.get(session, "name"), "Spirit")

    def test_set(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Storm"))
            backend = HorseBackend(1)
            backend.set(session, "name", "Mary")
            assert_equals(backend.get(session, "name"), "Mary")

    def test_pass_time(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Fury"))
            backend = HorseBackend(1)
            backend.pass_time(session, 200, False)
            assert_less(backend.get(session, "hygiene"), 100)

    def test_groom(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(hygiene=0, stimulation=0))
            backend = HorseBackend(1)
            backend.groom(session)
            assert_equals(backend.get(session, "hygiene"), 100)
            assert_greater(backend.get(session, "stimulation"), 0)

    def test_pet(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(stimulation=0))
            backend = HorseBackend(1)
            backend.pet(session)
            assert_greater(backend.get(session, "stimulation"), 0)

    def test_get_events(self):
        with DummyDB() as session:
            session.add(
                    HorseFactory.build(
                        food=100,
                        food_date=0,
                        food_time=0,
                        water=100,
                        water_date=0,
                        water_time=0))
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time", numeric=60)])
            backend = HorseBackend(1)
            now = time.get_time_stamp(session)
            backend.get_events(session, now)
            assert_greater(len(time._events), 0)
