import factory

from models.event import Event


class EventFactory(factory.Factory):
    class Meta:
        model = Event

    subject = factory.Sequence(lambda n: "Test-event-%d" % n)
    date = 0
    time = 0
    night = False

    @factory.post_generation
    def callbacks(self, create, extracted, **kwargs):
        if extracted:
            for callback in extracted:
                self.callbacks.append(callback)
