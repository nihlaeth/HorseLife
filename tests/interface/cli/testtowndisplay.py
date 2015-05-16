"""Test interface.cli.TownDisplay."""
from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from interface.cli.towndisplay import TownDisplay
from interface.cli.messagedisplay import MessageDisplay
from core.towncore import TownCore
from core.messagecore import MessageCore
from backend.session import SessionScope
from support.messages.quit import Quit
from support.messages.back import Back


class TestTownDisplay(object):

    """Test interface.cli.TownDisplay."""

    def test_init(self):
        """Test TownDisplay.__init__(core)."""
        display = TownDisplay("test")
        # pylint: disable=protected-access
        assert_equals(display._core, "test")

    @mock.patch("interface.cli.towndisplay.debug")
    @mock.patch.object(MessageDisplay, "display")
    @mock.patch.object(TownCore, "choice")
    @mock.patch.object(TownDisplay, "init")
    @mock.patch.object(SessionScope, "__enter__")
    def test_display(self, m_db, m_init, m_choice, m_msg, m_debug):
        """Test TownDisplay.display()."""
        with DummyDB() as session:
            m_db.return_value = session
            m_debug.return_value = False

            m_init.return_value = None
            display = TownDisplay(TownCore())

            # _choice is normally set by init
            # pylint: disable=protected-access
            display._choice = None

            quit_ = Quit()
            back = Back()
            m_choice.return_value = back
            assert_equals(display.display(), back)

            m_choice.return_value = quit_
            assert_equals(display.display(), quit_)

            m_choice.return_value = MessageCore()
            m_msg.return_value = quit_
            assert_equals(display.display(), quit_)
            m_msg.assert_called_once_with()
