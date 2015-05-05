"""Test Level."""
from nose.tools import assert_equals

from backend.level import Level
from tests.tools.dummydb import DummyDB
from tests.tools.settingfactory import SettingFactory
from support.messages.timestamp import TimeStamp
from backend.messagebackend import MessageBackend
from backend.settingbackend import SettingBackend


class TestLevel(object):

    """Test Level."""

    def test_init(self):
        """Test Level.__init__(session)."""
        with DummyDB() as session:
            session.add(SettingFactory(name="Experience"))
            level = Level(session)
            # pylint: disable=protected-access
            assert_equals(level._xp.id_, 1)

    def test_level(self):
        """Test Level.level(session)."""
        with DummyDB() as session:
            session.add(SettingFactory(name="Experience", numeric=1000))
            level = Level(session)
            assert_equals(level.level(session), 3)

    def test_add_xp(self):
        """Test Level.add_xp(session, t_stamp, xp)."""
        with DummyDB() as session:
            session.add(SettingFactory(name="Experience"))
            level = Level(session)
            level.add_xp(session, TimeStamp(0, 0), 500)
            setting = SettingBackend(session, 1)
            assert_equals(setting.get(session, None, "numeric"), 500)

    def test_level_up(self):
        """Test Level._level_up(self, session, level, t_stamp)."""
        with DummyDB() as session:
            session.add(SettingFactory(name="Experience"))
            level = Level(session)
            # pylint: disable=protected-access
            level._level_up(session, 1, TimeStamp(0, 0))
            assert_equals(len(MessageBackend.all(session)), 1)

            # Now make sure it won't die if there is no message for a
            # certain level.
            level._level_up(session, 100, TimeStamp(0, 0))
