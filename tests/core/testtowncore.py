from nose.tools import assert_equals
import mock

from support.messages.back import Back
from support.messages.quit import Quit
from support.messages.action import Action
from support.messages.command import Command
from backend.session import SessionScope
from interface.cli.towndisplay import TownDisplay
from core.contractercore import ContracterCore
from core.towncore import TownCore
from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory


class TestTownCore():
    @mock.patch.object(ContracterCore, "run")
    @mock.patch.object(TownDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_db, m_display, m_contracter):
        """ Test TownCore.run()"""
        with DummyDB() as session:
            m_db.return_value = session
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])

            # Test quit
            quit = Quit()
            m_display.return_value = quit
            core = TownCore()
            result = core.run()
            assert_equals(result, quit)

            # Test command
            m_display.return_value = Command("assert False")
            try:
                core.run()
            except AssertionError:
                assert True
            else:
                assert False

            # Test actions
            # For now, just test that nothing dies when picking these
            # actions.
            m_contracter.return_value = quit
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
                    quit]
            result = core.run()
            m_contracter.assert_called_once_with()
            assert_equals(result, quit)
