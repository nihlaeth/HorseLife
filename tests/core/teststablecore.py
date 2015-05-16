"""Test StableCore."""
from nose.tools import assert_equals, assert_is_none
import mock

from tests.tools.stablefactory import StableFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.stableitemfactory import StableItemFactory
from tests.tools.dummydb import DummyDB
from backend.stablebackend import StableBackend
from backend.horsebackend import HorseBackend
from support.messages.action import Action
from support.messages.timestamp import TimeStamp
from core.stablecore import StableCore
from core.core import Core


class TestStableCore(object):

    """Test StableCore."""

    def test_init(self):
        """Test StableCore.__init__(stable)."""
        core = StableCore("stable")
        # pylint: disable=protected-access
        assert_equals(core._stable, "stable")

    @mock.patch.object(Core, "get_info")
    def test_get_info(self, m_info):
        """Test StableCore.get_info(session)."""
        with DummyDB() as session:
            m_info.return_value = []
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                StableFactory(
                    horses=[HorseFactory()],
                    items=[
                        StableItemFactory(name="food"),
                        StableItemFactory(name="water")])])
            StableBackend(session, 1).get_events(session, TimeStamp(0, 0))
            HorseBackend(session, 1).get_events(session, TimeStamp(0, 0))
            core = StableCore(StableBackend(session, 1))

            info = core.get_info(session)

            assert_equals(len(info), 29)

    def test_get_actions(self):
        """Test StableCore.get_actions(session)."""
        with DummyDB() as session:
            session.add(StableFactory(
                horses=[HorseFactory()],
                items=[
                    StableItemFactory(name="food"),
                    StableItemFactory(name="water")]))
            core = StableCore(StableBackend(session, 1))
            actions = core.get_actions(session)
            assert_equals(len(actions), 3)
            # pylint: disable=protected-access
            core._horse = HorseBackend(session, 1)
            actions = core.get_actions(session)
            assert_equals(len(actions), 9)

    def test_choice(self):
        """Test StableCore.choice(session, choice)."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                SettingFactory(name="Experience"),
                StableFactory(horses=[HorseFactory()], items=[
                    StableItemFactory(name="food"),
                    StableItemFactory(name="water")])])
            now = TimeStamp(0, 0)
            StableBackend(session, 1).get_events(session, now)
            HorseBackend(session, 1).get_events(session, now)

            core = StableCore(StableBackend(session, 1))
            # pylint: disable=protected-access
            core._horse = HorseBackend(session, 1)

            result = core.choice(session, Action("clean", ""))
            assert_is_none(result)

            result = core.choice(session, Action("change name", ""))
            assert_equals(isinstance(result, Action), True)

            result = core.choice(session, Action("groom", ""))
            assert_is_none(result)

            result = core.choice(session, Action("feed", ""))
            assert_is_none(result)

            result = core.choice(session, Action("water", ""))
            assert_is_none(result)

            result = core.choice(session, Action("pet", ""))
            assert_is_none(result)
