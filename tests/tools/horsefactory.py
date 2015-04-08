import factory

from models.horse import Horse
from stablefactory import StableFactory


class HorseFactory(factory.Factory):
    class Meta:
        model = Horse

    name = "Bless"
    age = 50
    sex = "Mare"
    race = "Mixed Breed"
    color = "Black"
    location = "Stable"
    health_status = "healthy"

    health = 100
    food = 100
    water = 100
    happiness = 100
    energy = 100
    exercise = 100
    hygiene = 100
    stimulation = 100
    environment = 100
    social = 100

    stable = factory.SubFactory(StableFactory)
