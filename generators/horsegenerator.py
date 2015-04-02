import random
from sqlalchemy import func
import ConfigParser

from generator import Generator
from models.horse import Horse


class HorseGenerator(Generator):
    def __init__(self):
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/horses.cfg")

    def _gen_one(self, breed, training="none"):
        if breed == "random":
            breed = random.choice(self._config.sections())
        return Horse(
            name="Nameless",
            age="30",
            sex=random.choice(["mare", "stallion"]),
            race=breed,
            color=random.choice(["black", "appaloosa", "white", "roan"]),
            location="Stable",
            health_status="Healthy",
            health=100,
            food=100,
            water=100,
            happiness=100,
            energy=100,
            hygiene=100,
            stimulation=100,
            environment=100,
            social=100,
            endurance=0,
            strength=0,
            speed=0,
            trust=0,
            weight=500,
            jumping=0,
            dressage=0,
            western=0,
            racing=0,
            harness=0,
            natural_horsemanship=0,
            character="Easygoing, Stubborn, Trusting",
            gen_endurance=random.randint(
                self._config.getint(breed, "genetic_endurance_min"),
                self._config.getint(breed, "genetic_endurance_max")),
            gen_strength=random.randint(
                self._config.getint(breed, "genetic_strength_min"),
                self._config.getint(breed, "genetic_strength_max")),
            gen_speed=random.randint(
                self._config.getint(breed, "genetic_speed_min"),
                self._config.getint(breed, "genetic_speed_max")),
            gen_jumping=random.randint(
                self._config.getint(breed, "genetic_jumping_min"),
                self._config.getint(breed, "genetic_jumping_max")),
            gen_dressage=random.randint(
                self._config.getint(breed, "genetic_dressage_min"),
                self._config.getint(breed, "genetic_dressage_max")),
            gen_western=random.randint(
                self._config.getint(breed, "genetic_western_min"),
                self._config.getint(breed, "genetic_western_max")),
            gen_racing=random.randint(
                self._config.getint(breed, "genetic_racing_min"),
                self._config.getint(breed, "genetic_racing_max")),
            gen_harness=random.randint(
                self._config.getint(breed, "genetic_harness_min"),
                self._config.getint(breed, "genetic_harness_max")),
            gen_horsemanship=random.randint(
                self._config.getint(breed, "genetic_horsemanship_min"),
                self._config.getint(breed, "genetic_horsemanship_max")))

    def gen_many(self, session, n, breed="random"):
        result = []
        for i in range(n):
            result.append(self._gen_one(breed))
        session.add_all(result)
        return result
