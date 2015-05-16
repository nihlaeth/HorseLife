"""Test interface.cli.PastureDisplay."""
from nose.tools import assert_equals
import mock

from interface.cli.pasturedisplay import PastureDisplay
from tests.tools.dummydb import DummyDB
from tests.tools.pasturefactory import PastureFactory
from backend.session import SessionScope
from backend.pasturebackend import PastureBackend
from core.pasturecore import PastureCore
from support.messages.quit import Quit


class TestPastureDisplay(object):

    """Test interface.cli.PastureDisplay."""

    def test_init(self):
        """Test PastureDisplay.__init__(core)."""
        display = PastureDisplay("test")
        # pylint: disable=protected-access
        assert_equals(display._core, "test")

    @mock.patch("interface.cli.pasturedisplay.debug")
    @mock.patch.object(PastureDisplay, "init")
    @mock.patch.object(PastureCore, "choice")
    @mock.patch.object(SessionScope, "__enter__")
    def test_display(self, m_db, m_choice, m_init, m_debug):
        """Test PastureDisplay.display()."""
        with DummyDB() as session:
            m_debug.return_value = False
            m_db.return_value = session
            m_init.return_value = None
            quit_ = Quit()
            m_choice.return_value = quit_

            session.add(PastureFactory())

            display = PastureDisplay(PastureCore(PastureBackend(session, 1)))
            assert_equals(display.display(), quit_)
