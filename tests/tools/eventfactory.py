"""Event factory to simplify testing."""
import factory

from models.event import Event


class EventFactory(factory.Factory):

    """Event factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Event

    subject = factory.Sequence(lambda n: "Test-event-%d" % n)
    obj_id = 1
    date = 0
    time = 0

    # pylint: disable=unused-argument
    @factory.post_generation
    def callbacks(self, create, extracted, **kwargs):
        """If callback is specified, append it to callbacks[]."""
        if extracted:
            for callback in extracted:
                self.callbacks.append(callback)
