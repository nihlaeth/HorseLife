"""Test interface.cli.MessageDisplay."""
from nose.tools import assert_equals
import mock

from interface.cli.messagedisplay import MessageDisplay
from tests.tools.dummydb import DummyDB
from backend.session import SessionScope
from core.messagecore import MessageCore
from support.messages.quit import Quit


class TestMessageDisplay(object):

    """Test interface.cli.MessageDisplay."""

    def test_init(self):
        """Test MessageDisplay.__init__(core)."""
        display = MessageDisplay("test")
        # pylint: disable=protected-access
        assert_equals(display._core, "test")

    @mock.patch("interface.cli.messagedisplay.debug")
    @mock.patch.object(MessageDisplay, "init")
    @mock.patch.object(MessageCore, "choice")
    @mock.patch.object(SessionScope, "__enter__")
    def test_display(self, m_db, m_choice, m_init, m_debug):
        """Test MessageDisplay.display()."""
        with DummyDB() as session:
            m_debug.return_value = False
            m_db.return_value = session
            m_init.return_value = None
            quit_ = Quit()
            m_choice.return_value = quit_

            display = MessageDisplay(MessageCore())
            assert_equals(display.display(), quit_)
