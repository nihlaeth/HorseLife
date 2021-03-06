"""Generator for Horse models."""
import random
import ConfigParser

from generator import Generator
from horseskillgenerator import HorseSkillGenerator
from support.messages.timestamp import TimeStamp
from models.horse import Horse


class HorseGenerator(Generator):

    """Generator for Horse models."""

    def __init__(self):
        """Set up config parser."""
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/horses.cfg")

    # Arguments are supposed to be different from parent method.
    # pylint: disable=arguments-differ
    def _gen_one(self, breed, t_stamp, training="none"):
        """Generate single Horse model.

        breed - horse breed (also section in config)
        t_stamp - TimeStamp at which the horse is called into creation
         -> this is important for event generation
        training - Unimplemented to date
        """
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
            food_date=t_stamp.date,
            food_time=t_stamp.time,
            food_msg=False,
            water=100,
            water_date=t_stamp.date,
            water_time=t_stamp.time,
            water_msg=False,
            happiness=100,
            energy=100,
            energy_date=t_stamp.date,
            energy_time=t_stamp.time,
            hygiene=100,
            hygiene_date=t_stamp.date,
            hygiene_time=t_stamp.time,
            hygiene_msg=False,
            stimulation=100,
            stimulation_date=t_stamp.date,
            stimulation_time=t_stamp.time,
            stimulation_msg=False,
            exercise=100,
            exercise_date=t_stamp.date,
            exercise_time=t_stamp.time,
            exercise_msg=False,
            environment=100,
            social=100,
            social_date=t_stamp.date,
            social_time=t_stamp.time,
            social_msg=False,
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

    def gen_many(self, session, num, breed="random", t_stamp=TimeStamp(0, 0)):
        """Generate one or more Horse models.

        session -- sqlalchemy session
        num -- number of Horses to create
        breed -- horse breed / config section
        t_stamp -- TimeStamp object at which the horses are to be created
        --> this is important for event generation
        """
        result = []
        for _ in range(num):
            result.append(self._gen_one(breed, t_stamp=t_stamp))
        # generate skills for horses
        for horse in result:
            horse.skills = HorseSkillGenerator().gen_many(session, [horse.mid])
        session.add_all(result)
        session.flush()
        return result
