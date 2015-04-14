import factory

from models.stable import Stable


class StableFactory(factory.Factory):
    class Meta:
        model = Stable

    name = "TestStable"
    surface = 10
    outside_surface = 0
    light = 50
    capacity = 1

    cleanliness = 100
    cleanliness_date = 0
    cleanliness_time = 0

    @factory.post_generation
    def horses(self, create, extracted, **kwargs):
        """ If horses are specified, add them to self.horses[]"""
        if extracted:
            for horse in extracted:
                self.horses.append(horse)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        """ If any items are specified, add them to self.items[]"""
        if extracted:
            for item in extracted:
                self.items.append(item)
