from nose.tools import assert_equals
import mock

from tests.tools.settingfactory import SettingFactory
from tests.tools.dummydb import DummyDB
from backend.settingbackend import SettingBackend
from backend.session import session_scope
from support.messages.event import Event
from backend.time import Time, day


class TestTime():
    def test_get_day(self):
        print "Test Time._get_day()"
        with DummyDB() as session:
            session.add(SettingFactory(name="Date", numeric=0, text=""))
            print "-- basic functionality"
            t = Time()
            assert_equals(t.get_day(session), day.Monday)
            t._date.set(session, "numeric", 2)
            assert_equals(t.get_day(session), day.Wednesday)
            t._date.set(session, "numeric", 7)
            assert_equals(t.get_day(session), day.Monday)

    def test_get_time(self):
        print "Test Time._get_time()"
        with DummyDB() as session:
            session.add(SettingFactory(name="Time", numeric=0, text=""))
            print "--basic functionality"
            t = Time()
            assert_equals(t.get_time(session), "00:00")
            t._time.set(session, "numeric", 60)
            assert_equals(t.get_time(session), "01:00")
            t._time.set(session, "numeric", 90)
            assert_equals(t.get_time(session), "01:30")
            t._time.set(session, "numeric", 899)
            assert_equals(t.get_time(session), "14:59")

    def test_event(self):
        t = Time()
        event = Event(0, 0, self.test_event)
        t.event(event)
        assert_equals(t._events[0], event)

        # Now test sorting.
        event1 = Event(1, 23, self.test_event)
        event2 = Event(0, 22, self.test_event)
        t.event(event1)
        t.event(event2)
        assert_equals(t._events[0], event1)
        assert_equals(t._events[1], event2)

    def callback(self):
        pass

    def test_pass_time(self):
        with DummyDB() as session:
            session.add(SettingFactory(name="Time"))
            session.add(SettingFactory(name="Date"))
            t = Time()
            t.pass_time(session, 480)
            assert_equals(t.get_day(session), day.Monday)
            assert_equals(t.get_time(session), "08:00")

            t.pass_time(session, 1440)
            assert_equals(t.get_day(session), day.Tuesday)
            assert_equals(t.get_time(session), "08:00")

            # Now test night functionality:
            # 900 minutes puts us at 23:00, which is past
            # bedtime. We should end up at 07:00 the next day.
            t.pass_time(session, 900)
            assert_equals(t.get_day(session), day.Wednesday)
            assert_equals(t.get_time(session), "07:00")

            # Now test events!
            with mock.patch.object(TestTime, "callback") as mock_meth:
                event = Event(2, 480, self.callback)
                t.event(event)
                t.pass_time(session, 120)
                mock_meth.assert_called_once_with()

                assert_equals(len(t._events), 0)

                t.event(event)
                future_event = Event(23, 24, self.callback)
                t.event(future_event)

                t.pass_time(session, 10)

                assert_equals(len(t._events), 1)
                assert_equals(t._events[0], future_event)
