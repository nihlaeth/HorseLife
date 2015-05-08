"""Test PastureCore."""
from nose.tools import assert_equals
import mock

from tests.tools.pasturefactory import PastureFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.horsefactory import HorseFactory
from tests.tools.personfactory import PersonFactory
from tests.tools.dummydb import DummyDB
from backend.session import SessionScope
from backend.pasturebackend import PastureBackend
from backend.horsebackend import HorseBackend
from interface.cli.pasturedisplay import PastureDisplay
from support.messages.quit import Quit
from support.messages.action import Action
from support.messages.timestamp import TimeStamp
from core.pasturecore import PastureCore


class TestPastureCore(object):

    """Test PastureCore."""

    @mock.patch("core.pasturecore.debug")
    @mock.patch.object(PastureDisplay, "display")
    @mock.patch.object(SessionScope, "__enter__")
    def test_run(self, m_db, m_display, m_debug):
        """Test PastureCore.run()."""
        with DummyDB() as session:
            m_db.return_value = session
            pasture_raw = PastureFactory()
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                SettingFactory(name="Experience"),
                PersonFactory(),
                pasture_raw])

            m_debug.return_value = False

            pasture = PastureBackend(session, 1)
            pasture.get_events(session, TimeStamp(0, 0))

            # Test Quit
            quit_ = Quit()
            m_display.return_value = quit_

            core = PastureCore(PastureBackend(session, 1))

            # pylint: disable=invalid-name
            result = core.run()

            m_display.assert_called_once_with()
            assert_equals(result, quit_)

            # Now test actions
            # Get a horse in that pasture!
            session.add(HorseFactory(pasture=pasture_raw))
            HorseBackend(session, 1).get_events(session, TimeStamp(0, 0))

            # Get a fresh core instance, to make sure it processes the
            # horse we put in the pasture.
            core = PastureCore(PastureBackend(session, 1))

            # For now, just make sure nothing dies when performing
            # these actions. We're not testing their effect (yet).
            m_display.side_effect = [
                Action("clean", ""),
                Action("stable", "", [HorseBackend(session, 1)]),
                quit_]

            result = core.run()
            assert_equals(
                len(PastureBackend(session, 1).get(session, None, "horses")),
                0)
            assert_equals(result, quit_)
