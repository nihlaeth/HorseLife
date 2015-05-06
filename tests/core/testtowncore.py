"""Test TownCore."""
from nose.tools import assert_equals
import mock

from support.messages.quit import Quit
from support.messages.action import Action
from backend.session import SessionScope
from interface.cli.towndisplay import TownDisplay
from core.contractercore import ContracterCore
from core.towncore import TownCore
from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from tests.tools.personfactory import PersonFactory


class TestTownCore(object):

    """Test TownCore."""

    @mock.patch("core.towncore.debug")
    @mock.patch.object(ContracterCore, "run")
    @mock.patch.object(TownDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_db, m_display, m_contracter, m_debug):
        """Test TownCore.run()."""
        with DummyDB() as session:
            m_db.return_value = session
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                SettingFactory(name="Experience"),
                PersonFactory()])

            m_debug.return_value = False

            # Test quit_
            quit_ = Quit()
            m_display.return_value = quit_
            core = TownCore()
            result = core.run()
            assert_equals(result, quit_)

            # Test actions
            # For now, just test that nothing dies when picking these
            # actions.
            m_contracter.return_value = quit_
            m_display.side_effect = [
                Action("bank", ""),
                Action("horses", ""),
                Action("contracter", ""),
                Action("tack", ""),
                Action("food", ""),
                Action("newspaper", ""),
                Action("veterinarian", ""),
                Action("farrier", ""),
                Action("competitions", ""),
                Action("employment", ""),
                Action("education", ""),
                quit_]
            result = core.run()
            m_contracter.assert_called_once_with()
            assert_equals(result, quit_)
