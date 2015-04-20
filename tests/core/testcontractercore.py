from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from tests.tools.stablefactory import StableFactory
from generators.stablegenerator import StableGenerator
from interface.cli.contracterdisplay import ContracterDisplay
from backend.session import SessionScope
from core.contractercore import ContracterCore
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.command import Command
from support.messages.action import Action
from support.messages.timestamp import TimeStamp


class TestContracterCore():
    @mock.patch.object(StableGenerator, "gen_many")
    @mock.patch.object(ContracterDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_db, m_display, m_stablegen):
        """Test ContracterCore.run()"""
        with DummyDB() as session:
            m_db.return_value = session
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])

            # Test quit
            quit = Quit()
            m_display.return_value = quit
            core = ContracterCore()
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

            # Test buying a stable
            stable = StableFactory()
            session.add(stable)
            m_stablegen.return_value = [stable]
            m_display.side_effect = [
                    Action("stables", ""),
                    Action("buy-stable", "", ["Shed"]),
                    Action("home", ""),
                    quit]
            result = core.run()
            m_stablegen.assert_called_once_with(
                    session,
                    1,
                    "Shed",
                    TimeStamp(0, 0))
            assert_equals(result, quit)

            # Test other (unimplemented) actions:
            m_display.side_effect = [
                    Action("pastures", ""),
                    Action("arenas", ""),
                    Action("tack-feed", ""),
                    quit]
            result = core.run()
            assert_equals(result, quit)
