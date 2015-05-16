"""Test interface.cli.StableDisplay."""
from nose.tools import assert_equals
import mock

from interface.cli.stabledisplay import StableDisplay
from tests.tools.dummydb import DummyDB
from tests.tools.stablefactory import StableFactory
from backend.session import SessionScope
from backend.stablebackend import StableBackend
from core.stablecore import StableCore
from support.messages.quit import Quit


class TestStableDisplay(object):

    """Test interface.cli.StableDisplay."""

    def test_init(self):
        """Test StableDisplay.__init__(core)."""
        display = StableDisplay("test")
        # pylint: disable=protected-access
        assert_equals(display._core, "test")

    @mock.patch("interface.cli.stabledisplay.debug")
    @mock.patch.object(StableDisplay, "init")
    @mock.patch.object(StableCore, "choice")
    @mock.patch.object(SessionScope, "__enter__")
    def test_display(self, m_db, m_choice, m_init, m_debug):
        """Test StableDisplay.display()."""
        with DummyDB() as session:
            m_debug.return_value = False
            m_db.return_value = session
            m_init.return_value = None
            quit_ = Quit()
            m_choice.return_value = quit_

            session.add(StableFactory())

            display = StableDisplay(StableCore(StableBackend(session, 1)))
            assert_equals(display.display(), quit_)
