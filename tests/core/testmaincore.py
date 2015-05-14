"""Test MainCore."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from tests.tools.stablefactory import StableFactory
from tests.tools.pasturefactory import PastureFactory
from core.maincore import MainCore
from core.stablecore import StableCore
from core.towncore import TownCore
from core.pasturecore import PastureCore
from core.messagecore import MessageCore
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.action import Action


class TestMainCore(object):

    """Test MainCore."""

    def test_init(self):
        """Test MainCore.__init__()."""
        # If it doesn't die, we're good.
        MainCore()

    def test_get_actions(self):
        """Test MainCore.get_actions(session)."""
        with DummyDB() as session:
            session.add_all(StableFactory.build_batch(5))
            session.add_all(PastureFactory.build_batch(5))
            core = MainCore()
            actions = core.get_actions(session)

            assert_equals(isinstance(actions[0], TownCore), True)
            assert_equals(isinstance(actions[2], StableCore), True)
            assert_equals(isinstance(actions[9], PastureCore), True)

    def test_choice(self):
        """Test MainCore.choice(session, choice)."""
        with DummyDB() as session:
            core = MainCore()

            assert_equals(isinstance(core.choice(session, Back()), Back), True)
            assert_equals(isinstance(core.choice(session, Quit()), Quit), True)
            assert_equals(isinstance(
                core.choice(session, StableCore(2)),
                StableCore), True)
            assert_equals(isinstance(
                core.choice(session, Action("messages", "")),
                MessageCore), True)
