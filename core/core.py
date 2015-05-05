"""Interface to inherit from for *Core classes."""
from backend.storybackend import StoryBackend
from backend.time import Time
from backend.level import Level
from backend.messagebackend import MessageBackend
from support.messages.action import Action


class Core(object):

    """Common methods to inherit for *Core classes."""

    def __init__(self):
        """Get a display."""
        self._display = None
        self.story = None
        self._level = None

    def run(self):
        """Game logic.

        Get data through backend and frontend (interface
        / user input), and do stuff with it! Communicate back to backend
        and front-end, well, you get the picture.
        """
        pass

    def __str__(self):
        """Return string interpretation of object."""
        return "Core"

    def get_story(self, session):
        """Get appropriate story for this core class."""
        location = type(self).__name__
        self.story = StoryBackend.one(session, location)
        return self.story

    def mark_story(self, session):
        """Mark story as read."""
        self.story.mark_read(session)

    def _info(self, session):
        """Construct info block."""
        time = Time(session)
        info = []
        # Current date and time
        info.append(" ".join([
            "Day:",
            str(time.get_day(session)),
            str(time.get_time_stamp(session).date),
            "Time:",
            time.get_time(session)]))
        # Current level
        # TODO: add meter to show progress towards next level
        if self._level is None:
            self._level = Level(session)
        info.append(" ".join(["Level:", str(self._level.level(session))]))
        # Messages (how many unread?)
        messages = MessageBackend.all(session)
        unread = MessageBackend.unread(session)
        summary = " ".join(["You have", str(len(messages)), "messages"])
        if unread > 0:
            summary = " ".join([
                "!!!",
                summary,
                "and",
                str(unread),
                "unread messages"])
        info.append(summary)
        info.append(Action("messages", "Read messages"))
        return info
