from nose.tools import assert_equals

from support.messages.event import Event


class TestEvent():
    def test_basic(self):
        event = Event(0, 5, self.test_basic, "test")
        assert_equals(event.date, 0)
        assert_equals(event.time, 5)
        assert_equals(event.callback, self.test_basic)
        assert_equals(event.subject, "test")

    def test_comparison(self):
        event1 = Event(0, 0, self.test_basic, "")
        event2 = Event(0, 0, self.test_basic, "")
        event3 = Event(5, 0, self.test_basic, "")
        event4 = Event(0, 5, self.test_basic, "")
        event5 = Event(23, -2, self.test_basic, "")

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
