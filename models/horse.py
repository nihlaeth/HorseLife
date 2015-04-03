from base import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey


class Horse(Base):
    __tablename__ = 'horses'

    id = Column(Integer, primary_key=True)

    # basic info
    age = Column(Integer)
    sex = Column(String)
    race = Column(String)
    color = Column(String)
    name = Column(String)
    location = Column(String)
    health_status = Column(String)

    # active stats - change quickly
    health = Column(Float)
    food = Column(Float)
    water = Column(Float)
    happiness = Column(Float)
    energy = Column(Float)
    exercise = Column(Float)
    hygiene = Column(Float)
    stimulation = Column(Float)
    environment = Column(Float)
    social = Column(Float)

    # passive stats - change slowly
    endurance = Column(Integer)
    strength = Column(Integer)
    speed = Column(Integer)
    trust = Column(Integer)
    weight = Column(Integer)

    # skills
    jumping = Column(Integer)
    dressage = Column(Integer)
    western = Column(Integer)
    racing = Column(Integer)
    harness = Column(Integer)
    natural_horsemanship = Column(Integer)

    # traits (don't change over time, genetics)
    character = Column(String)
    gen_endurance = Column(Integer)
    gen_strength = Column(Integer)
    gen_speed = Column(Integer)
    gen_jumping = Column(Integer)
    gen_dressage = Column(Integer)
    gen_western = Column(Integer)
    gen_racing = Column(Integer)
    gen_harness = Column(Integer)
    gen_horsemanship = Column(Integer)

    stable_id = Column(Integer, ForeignKey('stables.id'))

    def pass_time(self, minutes, night):

        food_decay_time = 10
        water_decay_time = 5
        hygiene_decay_time = 20
        social_decay_time = 20
        energy_increase_time = 3

        self.food -= minutes / food_decay_time
        self.water -= minutes / water_decay_time
        self.hygiene -= minutes / hygiene_decay_time
        self.social -= minutes / social_decay_time

        if night:
            self.energy += minutes / energy_increase_time

        # boundary checks
        if self.energy > 100:
            self.energy = 100
        if self.food < 0:
            self.food = 0
        if self.water < 0:
            self.water = 0
        if self.hygiene < 0:
            self.hygiene = 0
        if self.social < 0:
            self.social = 0

        # TODO exercise need is dependent on a couple of things
        # TODO update health as some needs drop too low
        # TODO update happiness according to needs
        # TODO check if horse is actually in a stable during
        # the night

    def __str__(self):
        return self.name
