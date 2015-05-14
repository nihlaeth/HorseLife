"""Test MainDisplay of the command line interface."""
from nose.tools import assert_equals
import mock

from interface.cli.display import Display
from interface.cli.maindisplay import MainDisplay
from interface.cli.stabledisplay import StableDisplay
from interface.cli.pasturedisplay import PastureDisplay
from interface.cli.messagedisplay import MessageDisplay
from interface.cli.towndisplay import TownDisplay
from tests.tools.dummydb import DummyDB
from backend.session import SessionScope
from core.maincore import MainCore
from core.stablecore import StableCore
from core.pasturecore import PastureCore
from core.towncore import TownCore
from core.messagecore import MessageCore
from support.messages.quit import Quit
from support.messages.back import Back


class TestMaiDisplay(object):

    """Test interface.cli.MainDisplay."""

    def test_init(self):
        """Test MainCore.__init__(core)."""
        display = MainDisplay("maincore")
        # pylint: disable=protected-access
        assert_equals(display._core, "maincore")

    # Yup. Too many arguments, but that's mocks for you.
    # Too many mocks in a test does qualify as a code smell, but in this
    # case I think it's ok. MainDisplay is not meant to be isolated.
    # pylint: disable=too-many-arguments,too-many-locals
    @mock.patch("interface.cli.maindisplay.debug")
    @mock.patch.object(StableDisplay, "display")
    @mock.patch.object(PastureDisplay, "display")
    @mock.patch.object(TownDisplay, "display")
    @mock.patch.object(MessageDisplay, "display")
    @mock.patch.object(MainCore, "choice")
    @mock.patch.object(MainCore, "get_info")
    @mock.patch.object(MainCore, "get_menu")
    @mock.patch.object(MainCore, "get_actions")
    @mock.patch.object(MainCore, "get_story")
    @mock.patch.object(MainCore, "get_level")
    @mock.patch.object(Display, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_display(
            self,
            m_db,
            m_display,
            m_lvl,
            m_story,
            m_actions,
            m_menu,
            m_info,
            m_choice,
            m_msg,
            m_town,
            m_pasture,
            m_stable,
            m_debug):
        """Test MainCore.display()."""
        with DummyDB() as session:
            m_debug.return_value = False

            m_db.return_value = session
            m_lvl.return_value = 0
            m_story.return_value = []
            m_actions.return_value = []
            m_menu.return_value = []
            m_info.return_value = []

            back = Back()
            m_display.return_value = back

            m_msg.return_value = Back()
            m_town.return_value = Back()
            m_pasture.return_value = Back()
            m_stable.return_value = Back()

            quit_ = Quit()
            m_choice.side_effect = [
                StableCore(1),
                TownCore(),
                PastureCore(1),
                MessageCore(),
                None,
                quit_]

            result = MainDisplay(MainCore()).display()
            assert_equals(result, quit_)
            m_stable.assert_called_once_with()
            m_town.assert_called_once_with()
            m_pasture.assert_called_once_with()
            m_msg.assert_called_once_with()

            # Now test error raising
            m_town.return_value = "invalid response"
