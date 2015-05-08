"""Pasture factory to simplify testing."""
import factory

from models.pasture import Pasture


class PastureFactory(factory.Factory):

    """Pasture factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Pasture

    name = "TestPasture"
    surface = 50
    capacity = 1
    food = True

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
