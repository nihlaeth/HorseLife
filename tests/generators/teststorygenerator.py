"""Test StoryGenerator."""
from nose.tools import assert_equals, assert_greater

from tests.tools.dummydb import DummyDB
from generators.storygenerator import StoryGenerator


class TestStoryGenerator(object):

    """Test StoryGenerator."""

    def test_gen_one(self):
        """Test StoryGenerator._gen_one(text_id)."""
        story = StoryGenerator()._gen_one("welcome")
        assert_equals(story.text_id, "welcome")
        assert_equals(story.read, False)
        assert_equals(story.depends_on, "None")
        assert_equals(story.location, "MainCore")

    def test_gen_many(self):
        """Test StoryGenerator.gen_many(session)."""
        with DummyDB() as session:
            stories = StoryGenerator().gen_many(session)
            assert_greater(len(stories), 0)
