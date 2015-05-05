"""Test Time."""
from nose.tools import assert_equals
import mock
import datetime

from tests.tools.horsefactory import HorseFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory
from tests.tools.dummydb import DummyDB
from tests.tools.profiled import profiled
from backend.horsebackend import HorseBackend
from backend.stablebackend import StableBackend
from backend.time import Time, DAY
from models.horse import Horse
from support.messages.timestamp import TimeStamp


class TestTime(object):

    """Test Time."""

    def test_get_day(self):
        """Test Time.get_day(session)."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Date", numeric=0, text=""),
                SettingFactory(name="Time")])
            time = Time(session)
            # DAY members are dynamically generated.
            # pylint: disable=no-member
            assert_equals(time.get_day(session), DAY.Monday)
            # t._date.set(session, "numeric", 2)
            # assert_equals(t.get_day(session), DAY.Wednesday)
            # t._date.set(session, "numeric", 7)
            # assert_equals(t.get_day(session), DAY.Monday)

    def test_get_time(self):
        """Test Time.get_time(session)."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Time", numeric=0, text=""),
                SettingFactory(name="Date")])
            time = Time(session)
            assert_equals(time.get_time(session), "00:00")
            # t._time.set(session, "numeric", 60)
            # assert_equals(t.get_time(session), "01:00")
            # t._time.set(session, "numeric", 90)
            # assert_equals(t.get_time(session), "01:30")
            # t._time.set(session, "numeric", 899)
            # assert_equals(t.get_time(session), "14:59")

    def test_pass_time(self):
        """Test Time.pass_time(session)."""
        with DummyDB() as session:
            session.add(SettingFactory(name="Time"))
            session.add(SettingFactory(name="Date"))
            session.add(EventFactory(date=5000))

            # Members of DAY are generated dynamically.
            # pylint: disable=no-member
            time = Time(session)
            now = TimeStamp(0, 480)
            time.pass_time(session, now)
            assert_equals(time.get_day(session), DAY.Monday)
            assert_equals(time.get_time(session), "08:00")

            now.add_min(1440)
            time.pass_time(session, now)

            assert_equals(time.get_day(session), DAY.Tuesday)
            assert_equals(time.get_time(session), "08:00")

            # Now test night functionality:
            # 900 minutes puts us at 23:00, which is past
            # bedtime. We should end up at 07:00 the next day.

            now.add_min(900)
            time.pass_time(session, now)
            assert_equals(time.get_day(session), DAY.Wednesday)
            assert_equals(time.get_time(session), "07:00")

            # Now test events!
            with mock.patch.object(Horse, "event") as m_event:
                t_stamp = TimeStamp(1000, 0)
                m_event.return_value = {
                    "subject": "food",
                    "t_stamp": t_stamp}
                session.add(EventFactory(
                    subject="food",
                    callbacks=[CallbackFactory(
                        obj="HorseBackend",
                        obj_id=1)]))
                session.add(HorseFactory())

                now.add_min(120)
                time.pass_time(session, now)
                m_event.assert_called_once_with("food", TimeStamp(0, 0))

    def test_integration(self):
        """Test Time.pass_time integration with running system."""
        with DummyDB() as session:
            horse = HorseFactory()
            setting1 = SettingFactory(name="Date")
            setting2 = SettingFactory(name="Time")
            session.add_all([horse, setting1, setting2])

            time = Time(session)
            now = time.get_time_stamp(session)
            HorseBackend(session, 1).get_events(session, now)
            StableBackend(session, 1).get_events(session, now)

            now.add_min(480)
            time.pass_time(session, now)

            now.add_min(1440)
            time.pass_time(session, now)

    def test_performance(self):
        """Test Time.pass_time under load."""
        # Now test with multiple instances!
        with DummyDB() as session:
            # n and t# are fine names in this case!
            # pylint: disable=invalid-name
            n = 2  # Keep this low to reduce total testing time!
            t1 = datetime.datetime.now()
            session.add_all(HorseFactory.build_batch(n))
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])
            t = Time(session)
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

            now.add_min(480)
            t.pass_time(session, now)

            t4 = datetime.datetime.now()

            now.add_min(1440)
            with profiled(False):
                t.pass_time(session, now)

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
