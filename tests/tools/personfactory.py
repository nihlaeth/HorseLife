"""Person factory to simplify testing."""
import factory

from models.person import Person


class PersonFactory(factory.Factory):

    """Person factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Person

    name = factory.Sequence(lambda n: "Test%d" % n)
    age = 18
    money = 2000

    # pylint: disable=unused-argument
    @factory.post_generation
    def horses(self, create, extracted, **kwargs):
        """Populate the horses list."""
        if extracted:
            for horse in extracted:
                self.horses.append(horse)
