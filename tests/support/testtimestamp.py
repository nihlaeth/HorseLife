from nose.tools import assert_equals

from support.messages.timestamp import TimeStamp


class TestTimeStamp():
    def test_basic(self):
        t_stamp = TimeStamp(0, 5)
        assert_equals(t_stamp.date, 0)
        assert_equals(t_stamp.time, 5)

    def test_comparison(self):
        t_stamp1 = TimeStamp(0, 0)
        t_stamp2 = TimeStamp(0, 0)
        t_stamp3 = TimeStamp(5, 0)
        t_stamp4 = TimeStamp(0, 5)
        t_stamp5 = TimeStamp(23, 2)

        assert_equals(t_stamp1 == t_stamp2, True)
        assert_equals(t_stamp1 == t_stamp3, False)
        assert_equals(t_stamp1 == t_stamp4, False)
        assert_equals(t_stamp1 == t_stamp5, False)

        assert_equals(t_stamp1 != t_stamp2, False)
        assert_equals(t_stamp1 != t_stamp3, True)
        assert_equals(t_stamp1 != t_stamp4, True)
        assert_equals(t_stamp1 != t_stamp5, True)

        assert_equals(t_stamp1 < t_stamp2, False)
        assert_equals(t_stamp1 < t_stamp3, True)
        assert_equals(t_stamp3 < t_stamp4, False)
        assert_equals(t_stamp3 < t_stamp5, True)

        assert_equals(t_stamp1 <= t_stamp2, True)
        assert_equals(t_stamp1 <= t_stamp3, True)
        assert_equals(t_stamp3 <= t_stamp4, False)
        assert_equals(t_stamp3 <= t_stamp5, True)

        assert_equals(t_stamp1 > t_stamp2, False)
        assert_equals(t_stamp1 > t_stamp3, False)
        assert_equals(t_stamp3 > t_stamp4, True)
        assert_equals(t_stamp3 > t_stamp5, False)

        assert_equals(t_stamp1 >= t_stamp2, True)
        assert_equals(t_stamp1 >= t_stamp3, False)
        assert_equals(t_stamp3 >= t_stamp4, True)
        assert_equals(t_stamp3 >= t_stamp5, False)

        result1 = t_stamp3 + t_stamp4
        assert_equals(result1.date, 5)
        assert_equals(result1.time, 5)

        result2 = t_stamp5 - t_stamp4
        assert_equals(result2.date, 22)
        assert_equals(result2.time, 1437)

        assert_equals(t_stamp1 * 5, 0)
        assert_equals(t_stamp3 * 1, 300)
        assert_equals(t_stamp4 * 2, 10)

        assert_equals(t_stamp1 / 10, 0)
        assert_equals(t_stamp3 / 5, 60)
        assert_equals(t_stamp4 / 5, 1)

        assert_equals(t_stamp1.get_min(), 0)
        assert_equals(t_stamp3.get_min(), 300)
        assert_equals(t_stamp4.get_min(), 5)

        t_stamp1.add_min(10)
        assert_equals(t_stamp1.time, 10)
        t_stamp1.add_min(1440)
        assert_equals(t_stamp1.date, 1)
