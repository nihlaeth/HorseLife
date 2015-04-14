import factory

from models.event import Event


class EventFactory(factory.Factory):
    class Meta:
        model = Event

    subject = factory.Sequence(lambda n: "Test-event-%d" % n)
    obj_id = 1
    date = 0
    time = 0
    night = False

    @factory.post_generation
    def callbacks(self, create, extracted, **kwargs):
        """ If callback is specified, append it to callbacks[]."""
        if extracted:
            for callback in extracted:
                self.callbacks.append(callback)
