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
    food_date = 0
    food_time = 0

    water = 100
    water_date = 0
    water_time = 0

    happiness = 100

    energy = 100
    energy_date = 0
    energy_time = 0

    exercise = 100
    hygiene = 100

    stimulation = 100
    stimulation_date = 0
    stimulation_time = 0

    environment = 100

    social = 100
    social_date = 0
    social_time = 0

    stable = factory.SubFactory(StableFactory)
