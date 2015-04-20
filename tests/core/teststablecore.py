from nose.tools import assert_equals
import mock

from tests.tools.stablefactory import StableFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.dummydb import DummyDB
from backend.session import SessionScope
from backend.stablebackend import StableBackend
from backend.horsebackend import HorseBackend
from interface.cli.stabledisplay import StableDisplay
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.action import Action
from support.messages.command import Command
from support.messages.timestamp import TimeStamp
from core.stablecore import StableCore


class TestStableCore():
    @mock.patch.object(StableDisplay, "get_string")
    @mock.patch.object(StableDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_db, m_display, m_getstr):
        with DummyDB() as session:
            m_db.return_value = session
            stable_raw = StableFactory()
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                stable_raw])

            stable = StableBackend(1)
            stable.get_events(session, TimeStamp(0, 0))

            # Test Quit
            quit = Quit()
            m_display.return_value = quit

            core = StableCore(StableBackend(1))

            result = core.run()

            m_display.assert_called_once_with()
            assert_equals(result, quit)

            # Test Command
            m_display.return_value = Command("assert False")
            try:
                core.run()
            except AssertionError:
                assert True
            else:
                assert False

            # Now test actions
            # Get a horse in that stable!
            session.add(HorseFactory(stable=stable_raw))
            HorseBackend(1).get_events(session, TimeStamp(0, 0))
            m_getstr.return_value = "Bless"

            # Get a fresh core instance, to make sure it processes the
            # horse we put in the stable.
            core = StableCore(StableBackend(1))

            # For now, just make sure nothing dies when performing
            # these actions. We're not testing their effect (yet).
            m_display.side_effect = [
                    Action("clean", ""),
                    Action("feed", ""),
                    Action("water", ""),
                    Action("groom", ""),
                    Action("pet", ""),
                    Action("treat", ""),
                    Action("training journal", ""),
                    Action("pedigree", ""),
                    Action("change name", ""),
                    quit]
            result = core.run()
            assert_equals(result, quit)