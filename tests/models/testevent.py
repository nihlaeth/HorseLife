"""Test Event model."""
from nose.tools import assert_equals

from models.event import Event


class TestEvent(object):

    """Test Event model: models/event.py."""

    def test_basic(self):
        """Test Event.__init__()."""
        event = Event(0, 5, "test", 1)
        assert_equals(event.t_stamp.date, 0)
        assert_equals(event.t_stamp.time, 5)
        assert_equals(event.subject, "test")

    def test_comparison(self):
        """Test Event comparison methods."""
        event1 = Event(0, 0, "", 1)
        event2 = Event(0, 0, "", 1)
        event3 = Event(5, 0, "", 1)
        event4 = Event(0, 5, "", 1)
        event5 = Event(23, -2, "", 1)

        assert_equals(event1 == event2, True)
        assert_equals(event1 == event3, False)
        assert_equals(event1 == event4, False)
        assert_equals(event1 == event5, False)
        assert_equals(event1 is None, False)

        assert_equals(event1 != event2, False)
        assert_equals(event1 != event3, True)
        assert_equals(event1 != event4, True)
        assert_equals(event1 != event5, True)
        assert_equals(event1 is not None, True)

        assert_equals(event1 < event2, False)
        assert_equals(event1 < event3, True)
        assert_equals(event3 < event4, False)
        assert_equals(event3 < event5, True)
        assert_equals(event1 < None, False)

        assert_equals(event1 <= event2, True)
        assert_equals(event1 <= event3, True)
        assert_equals(event3 <= event4, False)
        assert_equals(event3 <= event5, True)
        assert_equals(event1 <= None, False)

        assert_equals(event1 > event2, False)
        assert_equals(event1 > event3, False)
        assert_equals(event3 > event4, True)
        assert_equals(event3 > event5, False)
        assert_equals(event1 > None, False)

        assert_equals(event1 >= event2, True)
        assert_equals(event1 >= event3, False)
        assert_equals(event3 >= event4, True)
        assert_equals(event3 >= event5, False)
        assert_equals(event1 >= None, False)
