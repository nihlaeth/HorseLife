from base import Base
from sqlalchemy import Column, Integer, String

class Horse(Base):
    __tablename__ = 'horses'

    id = Column(Integer, primary_key=True)

    # basic info
    age = Column(Integer)
    sex = Column(String)
    race = Column(String)
    color = Column(String)
    name = Column(String)
    location = Column(Integer)
    health_status = Column(String)

    # active stats - change quickly
    health = Column(Integer)
    food = Column(Integer)
    drink = Column(Integer)
    mood = Column(Integer)
    energy = Column(Integer)
    hygiene = Column(Integer)
    stimulation = Column(Integer)
    environment = Column(Integer)

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
    gen_enducance = Column(Integer)
    gen_strength = Column(Integer)
    gen_speed = Column(Integer)
    gen_jumping = Column(Integer)
    gen_dressage = Column(Integer)
    gen_western = Column(Integer)
    gen_racing = Column(Integer)
    gen_harness = Column(Integer)


