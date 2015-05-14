"""Test interface.cli.ContracterDisplay."""
from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from interface.cli.contracterdisplay import ContracterDisplay
from interface.cli.messagedisplay import MessageDisplay
from core.contractercore import ContracterCore
from core.messagecore import MessageCore
from backend.session import SessionScope
from support.messages.quit import Quit
from support.messages.back import Back


class TestContracterDisplay(object):

    """Test interface.cli.ContracterDisplay."""

    def test_init(self):
        """Test ContracterDisplay.__init__(core)."""
        display = ContracterDisplay("test")
        # pylint: disable=protected-access
        assert_equals(display._core, "test")

    @mock.patch("interface.cli.contracterdisplay.debug")
    @mock.patch.object(MessageDisplay, "display")
    @mock.patch.object(ContracterCore, "choice")
    @mock.patch.object(ContracterDisplay, "init")
    @mock.patch.object(SessionScope, "__enter__")
    def test_display(self, m_db, m_init, m_choice, m_msg, m_debug):
        """Test ContracterDisplay.display()."""
        with DummyDB() as session:
            m_db.return_value = session
            m_debug.return_value = False

            m_init.return_value = None
            display = ContracterDisplay(ContracterCore())

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
