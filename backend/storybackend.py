"""Provide abstraction layer for Story model."""
import ConfigParser

from backend import Backend
from models.story import Story
from support.messages.action import Action


class StoryBackend(Backend):

    """Abstraction layer for Story model.

    Unlike the other backend models, this one reads from config as well
    as the database.
    """

    @classmethod
    def all(cls, session):
        """Return a list of all story parts."""
        models = session.query(Story)
        return [StoryBackend(session, model.mid) for model in models]

    @classmethod
    def one(cls, session, location):
        """Return correct story for this location in this point of time.

        This checks to see if there are any story parts on this location,
        and if their dependencies have been met. If so, return the first.
        """
        # TODO actually perform the correct checks
        return StoryBackend(
            session,
            session.query(Story).filter_by(location=location)[0].mid)

    @classmethod
    def _one_id(cls, session, id_):
        """Return bare model - internal use only."""
        return session.query(Story).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Get story properties."""
        Backend.__init__(self, id_)
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/story.cfg")
        self.id_ = id_
        model = StoryBackend._one_id(session, id_)

        self.text_id = model.text_id
        self.text = self._config.get(self.text_id, "text")
        self.action = Action("story", "Dismiss")

    def mark_read(self, session):
        """Mark this story part as read."""
        StoryBackend._one_id(session, self.id_).read = True
