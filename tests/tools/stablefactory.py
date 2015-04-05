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

    @factory.post_generation
    def horses(self, create, extracted, **kwargs):
        if extracted:
            for horse in extracted:
                self.horses.append(horse)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if extracted:
            for item in extracted:
                self.items.append(item)
