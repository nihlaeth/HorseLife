"""Test PastureBackend."""
import mock
from nose.tools import assert_equals, assert_less, assert_greater

from backend.pasturebackend import PastureBackend
from backend.eventbackend import EventBackend
from models.pasture import Pasture
from support.messages.timestamp import TimeStamp
from tests.tools.dummydb import DummyDB
from tests.tools.pasturefactory import PastureFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.eventfactory import EventFactory
from tests.tools.callbackfactory import CallbackFactory
from tests.tools.settingfactory import SettingFactory


class TestPastureBackend(object):

    """Test PastureBackend."""

    def test_all_raw(self):
        """Test PastureBackend.all_raw(session)."""
        with DummyDB() as session:
            session.add_all(PastureFactory.build_batch(20))
            assert_equals(PastureBackend.all_raw(session).count(), 20)

    def test_all(self):
        """Test PastureBackend.all(session)."""
        with DummyDB() as session:
            pastures = PastureFactory.build_batch(3)
            session.add_all(pastures)
            backends = PastureBackend.all(session)
            assert_equals(backends[0].id_, 1)
            assert_equals(backends[2].id_, 3)

    def test_one_id(self):
        """Test PastureBackend._one_id(session, id)."""
        with DummyDB() as session:
            pastures = PastureFactory.build_batch(2)
            session.add_all(pastures)
            # The whole point here is to test a protected method.
            # pylint: disable=protected-access
            pasture = PastureBackend._one_id(session, 1)
            assert_equals(pasture.mid, 1)
            pasture = PastureBackend._one_id(session, 2)
            assert_equals(pasture.mid, 2)

    def test_get(self):
        """Test PastureBackend.get(session, timestamp, key)."""
        with DummyDB() as session:
            session.add(PastureFactory.build(
                name="Test1",
                horses=[HorseFactory()]))
            backend = PastureBackend(session, 1)
            backend.get_events(session, TimeStamp(0, 0))
            assert_equals(backend.get(session, None, "name"), "Test1")
            # Now see if cleanliness behaves as it should.
            time1 = TimeStamp(0, 0)
            time2 = TimeStamp(0, 120)
            assert_equals(backend.get(session, time1, "cleanliness"), 100)
            assert_less(backend.get(session, time2, "cleanliness"), 100)

    def test_set(self):
        """Test PastureBackend.set(session, key, value)."""
        with DummyDB() as session:
            session.add(PastureFactory.build(name="Test1"))
            backend = PastureBackend(session, 1)
            assert_equals(backend.get(session, None, "name"), "Test1")
            backend.set(session, "name", "Test2")
            assert_equals(backend.get(session, None, "name"), "Test2")

    def test_clean(self):
        """Test PastureBackend.clean(session, timestamp)."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Experience"),
                PastureFactory(cleanliness=0)])
            backend = PastureBackend(session, 1)
            backend.get_events(session, TimeStamp(0, 0))
            t_stamp = backend.clean(session, TimeStamp(0, 0))
            assert_equals(t_stamp.time, 60)
            assert_equals(backend.get(
                session,
                t_stamp,
                "cleanliness"), 100)

    def test_get_events(self):
        """Test PastureBackend.get_events(session, timestamp)."""
        with DummyDB() as session:
            session.add(PastureFactory())
            backend = PastureBackend(session, 1)
            backend.get_events(session, TimeStamp(0, 0))
            assert_greater(len(EventBackend.all(session)), 0)

    def test_update_event(self):
        """Test PastureBackend._update_event(session, e_info)."""
        with DummyDB() as session:
            session.add_all([
                PastureFactory(),
                EventFactory(subject="flub")])
            backend = PastureBackend(session, 1)

            # The whole point here is to test a protected method.
            # pylint: disable=protected-access
            backend._update_event(session, {
                "subject": "flub",
                "t_stamp": TimeStamp(5, 20),
                "msg": None})

            event = EventBackend(session, 1)
            assert_equals(event.get(session, None, "date"), 5)
            assert_equals(event.get(session, None, "time"), 20)

    def test_event_callback(self):
        """Test PastureBackend.event_callback(session, subject, timestamp)."""
        with DummyDB() as session:
            session.add_all([
                PastureFactory(),
                EventFactory(subject="pasturestest",
                             callbacks=[CallbackFactory(
                                 obj="PastureBackend",
                                 obj_id=1)])])
            with mock.patch.object(Pasture, "event") as m_event:
                m_event.return_value = {
                    "subject": "pasturestest",
                    "t_stamp": TimeStamp(1000, 0)}
                backend = PastureBackend(session, 1)
                t_stamp = TimeStamp(0, 0)
                backend.event_callback(session, "pasturestest", t_stamp)

                m_event.assert_called_once_with("pasturestest", t_stamp)
        # Now test it without the mock!
        with DummyDB() as session:
            session.add_all([
                PastureFactory()])
            backend = PastureBackend(session, 1)
            backend.get_events(session, TimeStamp(0, 0))
            t_stamp = TimeStamp(0, 0)
            backend.event_callback(session, "cleanliness", t_stamp)
            event = EventBackend.one(session, "cleanliness", 1)
            assert_greater(event.get(session, None, "time"), 0)
