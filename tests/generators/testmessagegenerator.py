"""Test MessageGenerator."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from support.messages.timestamp import TimeStamp
from generators.messagegenerator import MessageGenerator


class TestMessageGenerator(object):

    """Test MessageGenerator."""

    def test_gen_one(self):
        """Test MessageGenerator._gen_one(subject, t_stamp, text)."""
        # pylint: disable=protected-access
        message = MessageGenerator._gen_one("test", TimeStamp(0, 0), "Hey")
        assert_equals(message.subject, "test")
        assert_equals(message.date, 0)
        assert_equals(message.time, 0)
        assert_equals(message.text, "Hey")

    def test_gen_many(self):
        """Test MessageGenerator.gen_many(session, messages)."""
        with DummyDB() as session:
            messages = [
                {"subject": "t1", "t_stamp": TimeStamp(0, 0), "text": "1"},
                {"subject": "t2", "t_stamp": TimeStamp(5, 20), "text": "2"},
                {"subject": "t3", "t_stamp": TimeStamp(-1, 1), "text": "3"}]
            db_msgs = MessageGenerator.gen_many(session, messages)
            assert_equals(len(db_msgs), 3)
            assert_equals(db_msgs[0].subject, "t1")
            assert_equals(db_msgs[1].time, 20)
            assert_equals(db_msgs[2].text, "3")
