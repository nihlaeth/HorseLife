"""Test MessageCore."""
from nose.tools import assert_equals, assert_is_none
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.messagefactory import MessageFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.personfactory import PersonFactory
from support.messages.action import Action
from support.messages.quit import Quit
from support.messages.back import Back
from backend.session import SessionScope
from backend.messagebackend import MessageBackend
from core.core import Core
from core.messagecore import MessageCore
from interface.cli.messagedisplay import MessageDisplay


class TestMessageCore(object):

    """Test MessageCore."""

    def test_init(self):
        """Test MessageCore.__init__()."""
        # if it doesn't die, we're good
        MessageCore()

    def test_get_actions(self):
        """Test MessageCore.get_actions(session)."""
        with DummyDB() as session:
            core = MessageCore()

            session.add_all(MessageFactory.build_batch(5))
            actions = core.get_actions(session)
            assert_equals(len(actions), 5)

            # test message screen
            # pylint: disable=protected-access
            core._screen = "message"
            core._message = MessageBackend(session, 1)
            actions = core.get_actions(session)
            assert_equals(actions[0].action, "delete")
            assert_equals(actions[1].action, "mark-unread")

    @mock.patch.object(Core, "get_info")
    def test_get_info(self, m_info):
        """Test MessageCore.get_info(session)."""
        with DummyDB() as session:
            m_info.return_value = []
            core = MessageCore()
            assert_equals(len(core.get_info(session)), 0)

            # test message screen
            session.add(MessageFactory())
            # pylint: disable=protected-access
            core._screen = "message"
            core._message = MessageBackend(session, 1)

            info = core.get_info(session)

            assert_equals(len(info), 6)

    def test_choice(self):
        """Test MessageCore.choice(session, choice)."""
        with DummyDB() as session:
            core = MessageCore()
            
            # Back testing
            back = Back()
            assert_equals(core.choice(session, back), back)
            # pylint: disable=protected-access
            core._screen = "message"
            assert_is_none(core.choice(session, back))
            assert_equals(core._screen, "list")

            session.add(MessageFactory())
            # Action testing
            assert_is_none(core.choice(session, Action("message", "", [1])))
            assert_equals(core._screen, "message")

            assert_is_none(core.choice(session, Action("mark-unread", "")))
            assert_equals(
                MessageBackend(session, 1).get(session, None, "read"),
                False)

            assert_is_none(core.choice(session, Action("delete", "")))
            assert_equals(len(MessageBackend.all(session)), 0)
