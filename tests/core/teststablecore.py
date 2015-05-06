"""Test StableCore."""
from nose.tools import assert_equals
import mock
import datetime

from tests.tools.stablefactory import StableFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.stableitemfactory import StableItemFactory
from tests.tools.personfactory import PersonFactory
from tests.tools.dummydb import DummyDB
from tests.tools.profiled import profiled
from backend.session import SessionScope
from backend.stablebackend import StableBackend
from backend.horsebackend import HorseBackend
from interface.cli.stabledisplay import StableDisplay
from support.messages.quit import Quit
from support.messages.action import Action
from support.messages.timestamp import TimeStamp
from core.stablecore import StableCore


class TestStableCore(object):

    """Test StableCore."""

    @mock.patch("core.stablecore.debug")
    @mock.patch.object(StableDisplay, "get_string")
    @mock.patch.object(StableDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_db, m_display, m_getstr, m_debug):
        """Test StableCore.run()."""
        with DummyDB() as session:
            m_db.return_value = session
            stable_raw = StableFactory(items=[
                StableItemFactory(name="food"),
                StableItemFactory(name="water")])
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                SettingFactory(name="Experience"),
                PersonFactory(),
                stable_raw])

            m_debug.return_value = False

            stable = StableBackend(session, 1)
            stable.get_events(session, TimeStamp(0, 0))

            # Test Quit
            quit_ = Quit()
            m_display.return_value = quit_

            core = StableCore(StableBackend(session, 1))

            # pylint: disable=invalid-name
            t1 = datetime.datetime.now()
            result = core.run()
            t2 = datetime.datetime.now()

            m_display.assert_called_once_with()
            assert_equals(result, quit_)

            # Now test actions
            # Get a horse in that stable!
            session.add(HorseFactory(stable=stable_raw))
            HorseBackend(session, 1).get_events(session, TimeStamp(0, 0))
            m_getstr.return_value = "Bless"

            # Get a fresh core instance, to make sure it processes the
            # horse we put in the stable.
            core = StableCore(StableBackend(session, 1))

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
                quit_]

            t3 = datetime.datetime.now()
            with profiled(False):
                result = core.run()
            t4 = datetime.datetime.now()
            assert_equals(result, quit_)

            print "Test1:"
            print (t2 - t1).total_seconds()
            print "Test2:"
            print (t4 - t3).total_seconds()

            # assert False
