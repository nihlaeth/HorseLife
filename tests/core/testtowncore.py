"""Test TownCore."""
from nose.tools import assert_equals
import mock

from support.messages.action import Action
from core.core import Core
from core.contractercore import ContracterCore
from core.towncore import TownCore
from errors.invalidchoice import InvalidChoice


class TestTownCore(object):

    """Test TownCore."""

    def test_init(self):
        """Test TownCore.__init__()."""
        # If it doesn't die, we're good.
        TownCore()

    @mock.patch.object(Core, "get_info")
    def test_get_info(self, m_info):
        """Test TownCore.get_info(session)."""
        m_info.return_value = []
        core = TownCore()
        info = core.get_info(None)
        assert_equals(info[0], "Where do you want to visit?")

    def test_get_actions(self):
        """Test TownCore.get_actions(session)."""
        core = TownCore()
        actions = core.get_actions(None)
        assert_equals(len(actions), 11)

    def test_choice(self):
        """Test TownCore.choice(session, choice)."""
        core = TownCore()
        result = core.choice(None, Action("contracter", ""))
        assert_equals(isinstance(result, ContracterCore), True)

        try:
            result = core.choice(None, Action("unknown", ""))
        except InvalidChoice:
            assert True
        else:
            assert False
