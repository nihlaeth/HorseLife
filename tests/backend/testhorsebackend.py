from nose.tools import assert_equals, assert_less, assert_greater
import mock
import datetime

from backend.horsebackend import HorseBackend
from backend.eventbackend import EventBackend
from backend.time import time
from models.horse import Horse
from support.messages.timestamp import TimeStamp
from tests.tools.dummydb import DummyDB
from tests.tools.horsefactory import HorseFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory


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
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            assert_equals(backend.get(session, TimeStamp(0, 0), "name"),
                          "Spirit")

    def test_set(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Storm"))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            backend.set(session, "name", "Mary")
            assert_equals(backend.get(session, TimeStamp(0, 0), "name"),
                          "Mary")

    def test_pass_time(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Fury"))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            backend.pass_time(session, 200, False)
            assert_less(backend.get(session, TimeStamp(0, 0), "hygiene"),
                        100)

    def test_groom(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(hygiene=0, stimulation=0))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            backend.groom(session)
            t_stamp = TimeStamp(0, 0)
            assert_equals(backend.get(session, t_stamp, "hygiene"), 100)
            assert_greater(backend.get(session, t_stamp, "stimulation"), 0)

    def test_pet(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(stimulation=0))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            backend.pet(session)
            assert_greater(backend.get(session,
                                       TimeStamp(0, 0),
                                       "stimulation"), 0)

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
            assert_greater(len(EventBackend.all(session)), 0)

    def test_callback(self):
        with DummyDB() as session:
            t1 = datetime.datetime.now()
            session.add(HorseFactory.build())
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time", numeric=1430),
                EventFactory(
                    subject="food-test",
                    callbacks=[CallbackFactory(
                        obj="HorseBackend",
                        obj_id=1)])])
            t2 = datetime.datetime.now()
            with mock.patch.object(Horse, "event") as m:
                m.return_value = [
                        "food-test",
                        TimeStamp(1000, 0),
                        [["HorseBackend", 1]]]
                backend = HorseBackend(1)
                time.pass_time(session, 5)
                m.assert_called_once_with("food-test", TimeStamp(0, 0))
                assert_equals(EventBackend(1).get(session, "date"), 1000)
            t3 = datetime.datetime.now()
            # Now for real!
            backend = HorseBackend(1)
            now = time.get_time_stamp(session)
            t3_1 = datetime.datetime.now()
            backend.get_events(session, now)
            t3_2 = datetime.datetime.now()
            time.pass_time(session, 1440)
            t4 = datetime.datetime.now()
            t_stamp = time.get_time_stamp(session)
            assert_less(backend.get(session, t_stamp, "food"), 100)
            assert_less(backend.get(session, t_stamp, "water"), 100)
            assert_less(backend.get(session, t_stamp, "energy"), 100)
            t5 = datetime.datetime.now()

            print "Adding objects to session took:"
            print (t2 - t1).total_seconds()
            print "\n\n"
            print "Event injection test took:"
            print (t3 - t2).total_seconds()
            print "\n\n"
            print "Realistic event test took:"
            print (t4 - t3).total_seconds()
            print "-- setup took:"
            print (t3_1 - t3).total_seconds()
            print "-- get_events took:"
            print (t3_2 - t3_1).total_seconds()
            print "-- pass_time took:"
            print (t4 - t3_2).total_seconds()
            print "\n\n"
            print "Asserting realistic event test took:"
            print (t5 - t4).total_seconds()
            print "\n\n"
            print "Total test execution took:"
            print (t5 - t1).total_seconds()
            # assert False
            # TODO figure out why pass_time is so slow!
