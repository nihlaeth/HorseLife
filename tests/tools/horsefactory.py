import factory

from models.horse import Horse


class HorseFactory(factory.Factory):
    class Meta:
        model = Horse

    name = "Bless"
