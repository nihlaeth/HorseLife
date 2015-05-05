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

    # pylint: disable=arguments-differ
    @classmethod
    def one(cls, session, location, level):
        """Return correct story for this location in this point of time.

        This checks to see if there are any story parts on this location,
        and if their dependencies have been met. If so, return the first.
        """
        # Normally, you'd always use the 'is' operator to compare
        # to a boolean value. But sqlalchemy does not eat that.
        valid_stories = session.query(Story).filter(
            Story.location == location,
            Story.read == False,
            Story.level <= level)
        if valid_stories.count() < 1:
            return None
        # Now check dependencies
        for story in valid_stories:
            if story.depends_on == "None":
                return StoryBackend(session, story.mid)
            else:
                deps = story.depends_on.split(",")
                failed = False
                for dependency in deps:
                    read = StoryBackend._check_read(session, dependency)
                    if not read:
                        failed = True
                if not failed:
                    return StoryBackend(session, story.mid)
        return None

    @classmethod
    def _check_read(cls, session, text_id):
        """Test if story part has been read or not - internal use only."""
        story = session.query(Story).filter_by(text_id=text_id)[0]
        return story.read

    @classmethod
    def _one_id(cls, session, id_):
        """Return bare model - internal use only."""
        return session.query(Story).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Get story properties."""
        Backend.__init__(self, session, id_)
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/story.cfg")
        self.id_ = id_
        model = StoryBackend._one_id(session, id_)

        self.text_id = model.text_id
        self.text = self._config.get(self.text_id, "text")
        self.text = self.text.replace("\\n", "\n")
        self.action = Action("story", "Dismiss")

    def mark_read(self, session):
        """Mark this story part as read."""
        StoryBackend._one_id(session, self.id_).read = True
