"""Interface to inherit from for *Core classes."""
from backend.storybackend import StoryBackend


class Core(object):

    """Common methods to inherit for *Core classes."""

    def __init__(self):
        """Get a display."""
        self._display = None
        self.story = None

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
