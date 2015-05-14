"""Test ContracterCore."""
from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from tests.tools.personfactory import PersonFactory
from backend.stablebackend import StableBackend
from core.core import Core
from core.contractercore import ContracterCore
from support.messages.back import Back
from support.messages.action import Action


class TestContracterCore(object):

    """Test ContracterCore."""

    def test_init(self):
        """Test ContracterCore.__init__()."""
        # If it dies, there's a problem. Or something like that.
        ContracterCore()

    @mock.patch.object(Core, "get_info")
    def test_get_info(self, m_info):
        """Test ContracterCore.get_info(session)."""
        with DummyDB() as session:
            core = ContracterCore()

            # test home screen
            m_info.return_value = []
            info = core.get_info(session)

            assert_equals(info[0], "What do you want constructed?")

            # test stables screen
            # pylint: disable=protected-access
            core._screen = "stables"
            # get fresh list
            m_info.return_value = []
            info = core.get_info(session)

            assert_equals(info[0], "")
            assert_equals(info[1], "Shed")

    def test_get_actions(self):
        """Test ContracterCore.get_actions(session)."""
        core = ContracterCore()

        # test home screen
        actions = core.get_actions(None)

        assert_equals(actions[0].action, "stables")
        assert_equals(actions[1].action, "pastures")
        assert_equals(actions[2].action, "arenas")
        assert_equals(actions[3].action, "tack-feed")

        # test stables screen
        # pylint: disable=protected-access
        core._screen = "stables"
        actions = core.get_actions(None)

        assert_equals(actions[0].action, "buy-stable")
        assert_equals(actions[0].arguments[0], "Shed")

    def test_choice(self):
        """Test ContracterCore.choice(session, choice)."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Time"),
                SettingFactory(name="Date")])
            core = ContracterCore()

            # test back
            # pylint: disable=protected-access
            core._screen = "not-home"
            assert_equals(core.choice(session, Back()), None)
            assert_equals(core._screen, "home")

            # test switching screens
            assert_equals(core.choice(session, Action("arenas", "")), None)
            assert_equals(core._screen, "arenas")

            # test buying a stable
            session.add(PersonFactory())
            assert_equals(
                core.choice(session, Action("buy-stable", "", ["Shed", 500])),
                None)
            assert_equals(len(StableBackend.all(session)), 1)
