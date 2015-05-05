"""Generator for Story models."""
import ConfigParser

from generator import Generator
from models.story import Story


# pylint: disable=arguments-differ
class StoryGenerator(Generator):

    """Generator for Story models."""

    def __init__(self):
        """Setup config parser."""
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/story.cfg")

    def _gen_one(self, text_id):
        """Generate a single Story model."""
        return Story(
            text_id=text_id,
            read=False,
            depends_on=self._config.get(text_id, "depends_on"),
            location=self._config.get(text_id, "location"),
            level=self._config.get(text_id, "level"))

    def gen_many(self, session):
        """Generate all story parts in config as Story models."""
        result = []
        for text_id in self._config.sections():
            result.append(self._gen_one(text_id))
        session.add_all(result)
        session.flush()
        return result
