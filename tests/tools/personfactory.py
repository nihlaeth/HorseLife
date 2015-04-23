import factory

from models.person import Person


class PersonFactory(factory.Factory):
    class Meta:
        model = Person
    name = factory.Sequence(lambda n: "Test%d" % n)
    age = 18
    money = 10

    @factory.post_generation
    def horses(self, create, extracted, **kwargs):
        if extracted:
            for horse in extracted:
                self.horses.append(horse)
