"""Test StoryBackend."""
from nose.tools import assert_equals

from tests.tools.dummydb import DummyDB
from tests.tools.storyfactory import StoryFactory
from backend.storybackend import StoryBackend


class TestStoryBackend(object):

    """Test StoryBackend."""

    def test_all(self):
        """Test StoryBackend.all(session)."""
        with DummyDB() as session:
            session.add_all(StoryFactory.build_batch(20))
            backends = StoryBackend.all(session)
            assert_equals(len(backends), 20)

    def test_one(self):
        """Test StoryBackend.one(session, location)."""
        with DummyDB() as session:
            session.add(StoryFactory())
            backend = StoryBackend.one(session, "MainCore", 0)
            assert_equals(backend.id_, 1)

    def test_init(self):
        """Test StoryBackend.__init__(session, id)."""
        with DummyDB() as session:
            session.add(StoryFactory())
            backend = StoryBackend(session, 1)
            assert_equals(backend.id_, 1)

    def test_one_id(self):
        """Test StoryBackend._one_id(session, id)."""
        with DummyDB() as session:
            story = StoryFactory()
            session.add(story)
            # pylint: disable=protected-access
            result = StoryBackend._one_id(session, 1)
            assert_equals(story, result)

    def test_mark_read(self):
        """Test StoryBackend.mark_read(session)."""
        with DummyDB() as session:
            session.add(StoryFactory())
            backend = StoryBackend(session, 1)
            # pylint: disable=protected-access
            backend.mark_read(session)
            story = StoryBackend._one_id(session, 1)
            assert_equals(story.read, True)
