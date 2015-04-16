from nose.tools import assert_equals
import mock
import datetime

from tests.tools.horsefactory import HorseFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory
from tests.tools.dummydb import DummyDB
from tests.tools.profiled import profiled
from backend.settingbackend import SettingBackend
from backend.eventbackend import EventBackend
from backend.horsebackend import HorseBackend
from backend.stablebackend import StableBackend
from backend.time import Time, day
from models.horse import Horse
from support.messages.timestamp import TimeStamp


class TestTime():
    def test_get_day(self):
        """ Test Time.get_day(session)"""
        with DummyDB() as session:
            session.add(SettingFactory(name="Date", numeric=0, text=""))
            t = Time()
            assert_equals(t.get_day(session), day.Monday)
            t._date.set(session, "numeric", 2)
            assert_equals(t.get_day(session), day.Wednesday)
            t._date.set(session, "numeric", 7)
            assert_equals(t.get_day(session), day.Monday)

    def test_get_time(self):
        """ Test Time.get_time(session)"""
        with DummyDB() as session:
            session.add(SettingFactory(name="Time", numeric=0, text=""))
            t = Time()
            assert_equals(t.get_time(session), "00:00")
            t._time.set(session, "numeric", 60)
            assert_equals(t.get_time(session), "01:00")
            t._time.set(session, "numeric", 90)
            assert_equals(t.get_time(session), "01:30")
            t._time.set(session, "numeric", 899)
            assert_equals(t.get_time(session), "14:59")

    def test_pass_time(self):
        """ Test Time.pass_time(session)"""
        with DummyDB() as session:
            t1 = datetime.datetime.now()
            session.add(SettingFactory(name="Time"))
            session.add(SettingFactory(name="Date"))
            session.add(EventFactory(date=5000))
            t2 = datetime.datetime.now()

            t = Time()
            t.pass_time(session, 480)
            t3 = datetime.datetime.now()
            assert_equals(t.get_day(session), day.Monday)
            assert_equals(t.get_time(session), "08:00")
            t4 = datetime.datetime.now()

            t.pass_time(session, 1440)
            t5 = datetime.datetime.now()

            assert_equals(t.get_day(session), day.Tuesday)
            assert_equals(t.get_time(session), "08:00")
            t6 = datetime.datetime.now()

            # Now test night functionality:
            # 900 minutes puts us at 23:00, which is past
            # bedtime. We should end up at 07:00 the next day.

            t.pass_time(session, 900)
            t7 = datetime.datetime.now()
            assert_equals(t.get_day(session), day.Wednesday)
            assert_equals(t.get_time(session), "07:00")

            t8 = datetime.datetime.now()
            # Now test events!
            with mock.patch.object(Horse, "event") as m:
                t_stamp = TimeStamp(1000, 0)
                m.return_value = {
                        "subject": "food",
                        "t_stamp": t_stamp}
                session.add(EventFactory(
                    subject="food",
                    callbacks=[CallbackFactory(
                        obj="HorseBackend",
                        obj_id=1)]))
                session.add(HorseFactory())

                t.pass_time(session, 120)
                m.assert_called_once_with("food", TimeStamp(0, 0))
            t9 = datetime.datetime.now()

            print "Setup"
            print (t2 - t1).total_seconds()
            print "\n\n"
            print "Pass 480 minutes, 1 fake event"
            print (t3 - t2).total_seconds()
            print "\n\n"
            print "Pass 1440 minutes, 1 fake future event"
            print (t5 - t4).total_seconds()
            print "\n\n"
            print "Pass 900 minutes, 1 fake future event"
            print (t7 - t6).total_seconds()
            print "\n\n"
            print "Patch test"
            print (t9 - t8).total_seconds()
            print "\n\n"
            print "Total test time"
            print (t9 - t1).total_seconds()

            # assert False

    def test_integration(self):
        """ Test Time.pass_time integration with running system."""
        with DummyDB() as session:
            t1 = datetime.datetime.now()
            horse = HorseFactory()
            setting1 = SettingFactory(name="Date")
            setting2 = SettingFactory(name="Time")
            session.add_all([horse, setting1, setting2])

            t = Time()
            now = t.get_time_stamp(session)
            HorseBackend(1).get_events(session, now)
            StableBackend(1).get_events(session, now)

            t2 = datetime.datetime.now()
            t.pass_time(session, 480)
            t3 = datetime.datetime.now()

            t.pass_time(session, 1440)
            t4 = datetime.datetime.now()

            print "Testing with a single instance"
            print "Setup"
            print (t2 - t1).total_seconds()
            print "\n\n"
            print "Pass time until 08:00"
            print (t3 - t2).total_seconds()
            print "\n\n"
            print "Pass entire day"
            print (t4 - t3).total_seconds()
            print "\n\n"
            print "Total"
            print (t4 - t1).total_seconds()
            print "\n\n"

            # assert False
        # Now test with multiple instances!
        with DummyDB() as session:
            n = 2  # Keep this low to reduce total testing time!
            t1 = datetime.datetime.now()
            session.add_all(HorseFactory.build_batch(n))
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])
            t = Time()
            now = t.get_time_stamp(session)

            t2 = datetime.datetime.now()
            # Generate all the events needed
            horse_b = HorseBackend.all(session)
            stable_b = StableBackend.all(session)

            for horse in horse_b:
                horse.get_events(session, now)
            for stable in stable_b:
                stable.get_events(session, now)
            t3 = datetime.datetime.now()

            t.pass_time(session, 480)

            t4 = datetime.datetime.now()

            with profiled():
                t.pass_time(session, 1440)

            t5 = datetime.datetime.now()

            print "Testing with %d instances" % n
            print "Setup"
            print (t2 - t1).total_seconds()
            print "\n\n"
            print "Generate events"
            print (t3 - t2).total_seconds()
            print "\n\n"
            print "Pass time until 08:00"
            print (t4 - t3).total_seconds()
            print "\n\n"
            print "Pass entire day"
            print (t5 - t4).total_seconds()
            print "\n\n"
            print "Total"
            print (t5 - t1).total_seconds()

            # assert False
