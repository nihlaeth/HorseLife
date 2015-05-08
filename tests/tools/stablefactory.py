"""Stable factory to simplify testing."""
import factory

from models.stable import Stable


class StableFactory(factory.Factory):

    """Stable factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Stable

    name = "TestStable"
    surface = 10
    outside_surface = 0
    light = 50
    capacity = 1

    cleanliness = 100
    cleanliness_date = 0
    cleanliness_time = 0
    cleanliness_msg = False

    # pylint: disable=unused-argument
    @factory.post_generation
    def horses(self, create, extracted, **kwargs):
        """Populate horses list."""
        if extracted:
            for horse in extracted:
                self.horses.append(horse)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        """Populate items list."""
        if extracted:
            for item in extracted:
                self.items.append(item)
