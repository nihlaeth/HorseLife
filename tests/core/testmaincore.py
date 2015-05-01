"""Test MainCore."""
from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from tests.tools.stablefactory import StableFactory
from core.maincore import MainCore
from core.buildingcore import BuildingCore
from support.messages.quit import Quit
from backend.session import SessionScope
from interface.cli.maindisplay import MainDisplay


class TestMainCore(object):

    """Test MainCore."""

    @mock.patch("core.maincore.debug")
    @mock.patch.object(BuildingCore, "run")
    @mock.patch.object(MainDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_session, m_display, m_building, m_debug):
        """Test MainCore.run()."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time")])
            m_session.return_value = session
            m_debug.return_value = False
            quit_ = Quit()
            m_display.return_value = quit_

            core = MainCore()
            result = core.run()
            assert_equals(result, quit_)

            # Now test the stables part
            session.add_all(StableFactory.build_batch(5))
            m_building.return_value = quit_
            building = BuildingCore(2)
            m_display.return_value = building

            result = core.run()

            m_building.assert_called_once_with()
            assert_equals(result, quit_)
