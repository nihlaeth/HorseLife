from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from tests.tools.stablefactory import StableFactory
from core.maincore import MainCore
from core.buildingcore import BuildingCore
from support.messages.quit import Quit
from support.messages.command import Command
from backend.session import session_scope
from interface.cli.maindisplay import MainDisplay


class TestMainCore():
    @mock.patch.object(BuildingCore, "run")
    @mock.patch.object(MainDisplay, "display")
    @mock.patch.object(session_scope, "__enter__")
    def test_run(self, m_session, m_display, m_building):
        """ Test MainCore.run()"""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])
            m_session.return_value = session
            quit = Quit()
            m_display.return_value = quit

            core = MainCore()
            result = core.run()
            assert_equals(result, quit)

            # Now test the stables part
            session.add_all(StableFactory.build_batch(5))
            m_building.return_value = quit
            building = BuildingCore(2)
            m_display.return_value = building

            result = core.run()

            m_building.assert_called_once_with()
            assert_equals(result, quit)

            # Test command
            m_display.return_value = Command("assert False")

            try:
                core.run()
            except AssertionError:
                # It worked
                pass
            else:
                assert False
