"""Horse factory to simplify testing."""
import factory

from models.horse import Horse
from stablefactory import StableFactory


class HorseFactory(factory.Factory):

    """Horse factory to simplify testing."""

    class Meta(object):

        """Meta class."""

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
    food_msg = False

    water = 100
    water_date = 0
    water_time = 0
    water_msg = False

    happiness = 100

    energy = 100
    energy_date = 0
    energy_time = 0

    exercise = 100
    exercise_date = 0
    exercise_time = 0

    hygiene = 100
    hygiene_date = 0
    hygiene_time = 0

    stimulation = 100
    stimulation_date = 0
    stimulation_time = 0
    stimulation_msg = False

    environment = 100

    social = 100
    social_date = 0
    social_time = 0

    stable = factory.SubFactory(StableFactory)
