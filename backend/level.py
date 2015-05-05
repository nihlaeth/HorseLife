"""Level system."""
import ConfigParser
import math

from settingbackend import SettingBackend
from generators.messagegenerator import MessageGenerator


class Level(object):

    """Level system."""

    def __init__(self, session):
        """Get SettingBackend object for experience setting."""
        self._xp = SettingBackend.one(session, "Experience")
        self._last_level = self.level(session)

    def level(self, session):
        """Translate experience into a level."""
        experience = self._xp.get(session, None, "numeric")
        return int(math.sqrt(float(experience)) / 31.)

    # xp is universally understood.
    # pylint: disable=invalid-name
    def add_xp(self, session, now, xp):
        """Increase experience."""
        experience = self._xp.get(session, None, "numeric")
        self._xp.set(session, "numeric", experience + xp)
        current_level = self.level(session)
        if current_level > self._last_level:
            self._level_up(session, current_level, now)

    def _level_up(self, session, level, now):
        """Perform actions associated with leveling up."""
        config = ConfigParser.SafeConfigParser()
        config.read("config/levels.cfg")
        sections = config.sections()
        for level in range(self._last_level + 1, level + 1):
            if str(level) in sections:
                msg = {
                    "subject": config.get(str(level), "subject"),
                    "t_stamp": now,
                    "text": config.get(str(level), "text")}
                MessageGenerator.gen_many(session, [msg])
        self._last_level = level
