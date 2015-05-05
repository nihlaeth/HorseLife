"""Factory for Story model to simplify testing."""
import factory

from models.story import Story


class StoryFactory(factory.Factory):

    """Factory for Story model to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Story
    text_id = "welcome"
    read = False
    location = "MainCore"
    depends_on = "None"
    level = 0
