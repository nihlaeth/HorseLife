"""Test EventGenerator."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from support.messages.timestamp import TimeStamp
from generators.eventgenerator import EventGenerator
from backend.eventbackend import EventBackend


class TestEventGenerator(object):

    """Test EventGenerator."""

    def test_gen_one(self):
        """Test EventGenerator._gen_one(subject, obj_id, tstamp, callbacks)."""
        # It's exactly the point to test a protected member...
        # pylint: disable=protected-access
        event = EventGenerator._gen_one(
            "test-event",
            1,
            TimeStamp(0, 0),
            [["TestEventGenerator", 1]])
        assert_equals(event.subject, "test-event")
        assert_equals(event.t_stamp, TimeStamp(0, 0))
        assert_equals(event.callbacks[0].obj, "TestEventGenerator")
        assert_equals(event.callbacks[0].obj_id, 1)

    def test_gen_many(self):
        """Test EventGenerator.gen_many(session, events)."""
        with DummyDB() as session:
            time1 = TimeStamp(0, 0)
            e_info = {
                "test1": {"obj_id": 1, "t_stamp": time1, "callbacks": []},
                "test2": {"obj_id": 2, "t_stamp": time1, "callbacks": []},
                "test3": {"obj_id": 3, "t_stamp": time1, "callbacks": []}}
            EventGenerator.gen_many(session, e_info)
            events = EventBackend.all(session)
            assert_equals(len(events), 3)
