"""Test PastureCore."""
from nose.tools import assert_equals, assert_is_none, assert_greater
import mock

from tests.tools.pasturefactory import PastureFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.dummydb import DummyDB
from backend.pasturebackend import PastureBackend
from backend.horsebackend import HorseBackend
from backend.time import Time
from support.messages.action import Action
from core.core import Core
from core.pasturecore import PastureCore


class TestPastureCore(object):

    """Test PastureCore."""

    def test_init(self):
        """Test PastureCore.__init__()."""
        core = PastureCore("pasture")
        # pylint: disable=protected-access
        assert_equals(core._pasture, "pasture")

    @mock.patch.object(Core, "get_info")
    def test_get_info(self, m_info):
        """Test PastureCore.get_info(session)."""
        with DummyDB() as session:
            m_info.return_value = []
            session.add_all([
                PastureFactory(),
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])
            core = PastureCore(PastureBackend(session, 1))
            info = core.get_info(session)

            assert_equals(len(info), 3)

    def test_get_actions(self):
        """Test PastureCore.get_actions(session)."""
        with DummyDB() as session:
            session.add(PastureFactory(horses=HorseFactory.build_batch(5)))
            core = PastureCore(PastureBackend(session, 1))
            actions = core.get_actions(session)

            assert_equals(len(actions), 6)

    def test_choice(self):
        """Test PastureCore.choice(session, choice)."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                PastureFactory(horses=HorseFactory.build_batch(5)),
                SettingFactory(name="Experience")])
            time = Time(session)
            now = time.get_time_stamp(session)
            horses = HorseBackend.all(session)
            for horse in horses:
                horse.get_events(session, now)
            PastureBackend(session, 1).get_events(session, now)
            core = PastureCore(PastureBackend(session, 1))

            result = core.choice(session, Action("clean", ""))
            assert_is_none(result)
            now = time.get_time_stamp(session)
            assert_greater(now.time, 0)

            result = core.choice(
                session,
                Action("stable", "", [HorseBackend(session, 1)]))

            horses = PastureBackend(session, 1).get(session, now, "horses")
            assert_equals(len(horses), 4)
