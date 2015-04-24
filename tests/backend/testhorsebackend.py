from nose.tools import assert_equals, assert_less, assert_greater
import mock
import datetime

from backend.horsebackend import HorseBackend
from backend.eventbackend import EventBackend
from backend.time import Time
from models.horse import Horse
from support.messages.timestamp import TimeStamp
from tests.tools.dummydb import DummyDB
from tests.tools.profiled import profiled
from tests.tools.horsefactory import HorseFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory


class TestHorseBackend():
    def test_init(self):
        """ Test HorseBackend.__init__(id)"""
        assert_equals(HorseBackend(1).id_, 1)

    def test_one_id(self):
        """ Test HorseBackend._one_id(session, id)"""
        with DummyDB() as session:
            session.add(HorseFactory.build())
            assert_equals(HorseBackend._one_id(session, 1).id, 1)

    def test_all_raw(self):
        """ Test HorseBackend.all_raw(session)"""
        with DummyDB() as session:
            session.add_all(HorseFactory.build_batch(20))
            assert_equals(HorseBackend.all_raw(session).count(), 20)

    def test_all(self):
        """ Test HorseBackend.all(session)"""
        with DummyDB() as session:
            horses = HorseFactory.build_batch(10)
            session.add_all(horses)
            backends = HorseBackend.all(session)
            assert_equals(len(backends), 10)

    def test_get(self):
        """ Test HorseBackend.get(session, timestamp, key)"""
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Spirit"))
            session.add(HorseFactory.build())
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            backend.get_events(session, TimeStamp(0, 0))
            backend2 = HorseBackend(2)
            backend2.get_events(session, TimeStamp(0, 0))
            assert_equals(backend.get(session, TimeStamp(0, 0), "name"),
                          "Spirit")
            # Now test the changing attributes (needs)
            t = TimeStamp
            assert_equals(backend.get(session, t(0, 0), "food"), 100)
            assert_less(backend.get(session, t(0, 120), "food"), 100)
            assert_equals(backend.get(session, t(0, 0), "water"), 100)
            assert_less(backend.get(session, t(0, 120), "water"), 100)
            assert_equals(backend.get(session, t(0, 0), "energy"), 100)
            # It was just night, energy should be restored.
            assert_equals(backend.get(session, t(0, 120), "energy"), 100)
            # At the end of the day, energy should be low
            assert_less(backend.get(session, t(0, 1319), "energy"), 50)
            # And in the morning, it should be restored again
            assert_greater(backend.get(session, t(1, 419), "energy"), 95)
            assert_equals(backend.get(session, t(0, 0), "stimulation"), 100)
            assert_greater(
                    EventBackend.one(
                        session,
                        "stimulation",
                        1).get(session, "time"),
                    0)
            # Stimulation does not decay during the night!
            assert_equals(backend.get(
                session,
                t(0, 120),
                "stimulation"), 100)
            assert_equals(backend2.get(session, t(0, 0), "stimulation"), 100)
            assert_equals(backend2.get(session, t(0, 120), "stimulation"), 100)
            assert_equals(backend.get(session, t(0, 0), "social"), 100)
            assert_less(backend.get(session, t(0, 120), "social"), 100)
            assert_equals(backend.get(session, t(0, 0), "exercise"), 100)
            assert_less(backend.get(session, t(0, 120), "exercise"), 100)
            assert_equals(backend.get(session, t(0, 0), "hygiene"), 100)
            assert_less(backend.get(session, t(0, 120), "hygiene"), 100)

    def test_set(self):
        """ Test HorseBackend.set(session, key, value)"""
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Storm"))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time")])
            backend = HorseBackend(1)
            backend.set(session, "name", "Mary")
            assert_equals(backend.get(session, TimeStamp(0, 0), "name"),
                          "Mary")

    def test_groom(self):
        """ Test HorseBackend.groom(session, timestamp)"""
        with DummyDB() as session:
            session.add(HorseFactory.build(hygiene=0, stimulation=0))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time"),
                             EventFactory(subject="stimulation"),
                             EventFactory(subject="hygiene")])
            backend = HorseBackend(1)
            t_stamp = backend.groom(session, TimeStamp(0, 0))
            assert_equals(t_stamp.time, 30)
            assert_equals(backend.get(session, t_stamp, "hygiene"), 100)
            assert_greater(backend.get(session, t_stamp, "stimulation"), 0)

    def test_pet(self):
        """ Test HorseBackend.pet(session, timestamp)"""
        with DummyDB() as session:
            session.add(HorseFactory.build(stimulation=0))
            session.add_all([SettingFactory(name="Date"),
                             SettingFactory(name="Time"),
                             EventFactory(subject="stimulation")])
            backend = HorseBackend(1)
            t_stamp = backend.pet(session, TimeStamp(0, 0))
            assert_equals(t_stamp.time, 5)
            assert_greater(backend.get(session, t_stamp, "stimulation"), 0)

    def test_get_events(self):
        """ Test HorseBackend.get_events(session, timestamp)"""
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
            time = Time(session)
            now = time.get_time_stamp(session)
            backend.get_events(session, now)
            assert_greater(len(EventBackend.all(session)), 0)

    def test_callback(self):
        """ Test HorseBackend.event_callback(session, subject, timestamp)"""
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
                m.return_value = {
                        "subject": "food-test",
                        "t_stamp": TimeStamp(1000, 0)}
                backend = HorseBackend(1)
                backend.event_callback(session, "food-test", TimeStamp(0, 0))
                m.assert_called_once_with("food-test", TimeStamp(0, 0))
        with DummyDB() as session:
            session.add_all([
                HorseFactory(),
                EventFactory(subject="food", obj_id="1")])
            backend = HorseBackend(1)
            with profiled():
                e_info = backend.event_callback(
                        session,
                        "food",
                        TimeStamp(0, 0))
            assert_equals(e_info["subject"], "food")
            assert_equals(e_info["t_stamp"].date, 0)
            assert_greater(e_info["t_stamp"].time, 0)
            # assert False

        with DummyDB() as session:
            # Now for real!
            session.add_all([
                HorseFactory(),
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])
            t3 = datetime.datetime.now()
            backend = HorseBackend(1)
            time = Time(session)
            now = time.get_time_stamp(session)
            t3_1 = datetime.datetime.now()
            backend.get_events(session, now)
            t3_2 = datetime.datetime.now()
            now.add_min(1440)
            time.pass_time(session, now)
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
