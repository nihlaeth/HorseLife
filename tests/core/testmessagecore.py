"""Test MessageCore."""
from nose.tools import assert_equals
import mock

from tests.tools.dummydb import DummyDB
from tests.tools.messagefactory import MessageFactory
from tests.tools.settingfactory import SettingFactory
from tests.tools.personfactory import PersonFactory
from support.messages.action import Action
from support.messages.quit import Quit
from support.messages.back import Back
from backend.session import SessionScope
from core.messagecore import MessageCore
from interface.cli.messagedisplay import MessageDisplay


class TestMessageCore(object):

    """Test MessageCore."""

    @mock.patch("core.messagecore.debug")
    @mock.patch.object(SessionScope, "__enter__")
    @mock.patch.object(MessageDisplay, "display")
    def test_run(self, m_display, m_db, m_debug):
        """Test MessageCore.run()."""
        with DummyDB() as session:
            messages = MessageFactory.build_batch(20)
            session.add_all(messages)
            session.add_all([
                SettingFactory(name="Date"),
                SettingFactory(name="Time"),
                SettingFactory(name="Experience"),
                PersonFactory()])
            quit_ = Quit()

            m_debug.return_value = False

            m_db.return_value = session

            # Test quit!
            m_display.return_value = quit_
            core = MessageCore()
            result = core.run()
            assert_equals(result, quit_)

            # Test reading a message, doing a bunch of other actions and
            # then pressing back two times - once delete is implemented,
            # we'll only need one back
            back1 = Back()
            back2 = Back()
            m_display.side_effect = [
                Action("message", "", [1]),
                Action("mark-unread", "", [1]),
                Action("delete", "", [1]),
                back1,
                back2]
            result = core.run()
            assert_equals(result, back2)
