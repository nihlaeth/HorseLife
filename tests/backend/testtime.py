from nose.tools import assert_equals
import mock

from models.setting import Setting
from backend.settingsbackend import SettingsBackend
from backend.session import session_scope


class TestTime():
    def test_get_day(self):
        print "Test Time._get_day()"
        with mock.patch.object(SettingsBackend, "one") as mock_multi:
            mock_multi.return_value = Setting(
                                            name="Date",
                                            numeric=0,
                                            text="")
            from backend.time import Time, day
            print "-- basic functionality"
            t = Time()
            assert_equals(t.get_day(), day.Monday)
            t._date.numeric = 2
            assert_equals(t.get_day(), day.Wednesday)
            t._date.numeric = 7
            assert_equals(t.get_day(), day.Monday)

    def test_get_time(self):
        print "Test Time._get_time()"
        with mock.patch.object(SettingsBackend, "one") as mock_multi:
            mock_multi.return_value = Setting(
                                            name="Time",
                                            numeric=0,
                                            text="")
            print "--basic functionality"
            from backend.time import Time, day
            t = Time()
            assert_equals(t.get_time(), "00:00")
            t._time.numeric = 60
            assert_equals(t.get_time(), "01:00")
            t._time.numeric = 90
            assert_equals(t.get_time(), "01:30")
            t._time.numeric = 899
            assert_equals(t.get_time(), "14:59")
