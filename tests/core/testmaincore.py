"""Test MainCore."""
from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from tests.tools.stablefactory import StableFactory
from tests.tools.personfactory import PersonFactory
from tests.tools.pasturefactory import PastureFactory
from core.maincore import MainCore
from core.buildingcore import BuildingCore
from core.towncore import TownCore
from core.pasturecore import PastureCore
from support.messages.quit import Quit
from support.messages.back import Back
from backend.session import SessionScope
from interface.cli.maindisplay import MainDisplay


class TestMainCore(object):

    """Test MainCore."""

    # We need all the mocks, and this is preferable to several layers
    # of nesting that are needed when we use context managers.
    # pylint: disable=too-many-arguments
    @mock.patch("core.maincore.debug")
    @mock.patch.object(PastureCore, "run")
    @mock.patch.object(TownCore, "run")
    @mock.patch.object(BuildingCore, "run")
    @mock.patch.object(MainDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(
            self,
            m_session,
            m_display,
            m_building,
            m_town,
            m_pasture,
            m_debug):
        """Test MainCore.run()."""
        with DummyDB() as session:
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                SettingFactory(name="Experience"),
                PersonFactory()])
            m_session.return_value = session
            m_debug.return_value = False
            quit_ = Quit()
            m_display.return_value = quit_

            core = MainCore()
            result = core.run()
            assert_equals(result, quit_)

            # Now test the stables part
            session.add_all(StableFactory.build_batch(5))
            session.add_all(PastureFactory.build_batch(5))
            back = Back()
            m_building.return_value = back
            m_town.return_value = back
            m_pasture.return_value = back
            building = BuildingCore(2)
            m_display.side_effect = [
                building,
                TownCore(),
                PastureCore(1),
                quit_]

            result = core.run()

            m_building.assert_called_once_with()
            m_town.assert_called_once_with()
            m_pasture.assert_called_once_with()
            assert_equals(result, quit_)
