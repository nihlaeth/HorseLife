import copy
from sqlalchemy import Column, Integer, Float, String, ForeignKey

from base import Base
from models.stable import Stable
from support.messages.timestamp import TimeStamp


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

    # active stats / needs - change quickly
    # Date and time indicate when the meter
    # has last been updated.
    health = Column(Float)

    food = Column(Float)
    food_date = Column(Integer)
    food_time = Column(Integer)

    water = Column(Float)
    water_date = Column(Integer)
    water_time = Column(Integer)

    happiness = Column(Float)

    energy = Column(Float)
    energy_date = Column(Integer)
    energy_time = Column(Integer)

    exercise = Column(Float)
    exercise_date = Column(Integer)
    exercise_time = Column(Integer)

    hygiene = Column(Float)
    hygiene_date = Column(Integer)
    hygiene_time = Column(Integer)

    stimulation = Column(Float)
    stimulation_date = Column(Integer)
    stimulation_time = Column(Integer)

    environment = Column(Float)

    social = Column(Float)
    social_date = Column(Integer)
    social_time = Column(Integer)

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

    def groom(self, skill="normal"):
        # TODO have skill factor into grooming
        # from backend.time import time
        # time.pass_time(30)
        self.stimulation += 40
        self.hygiene = 100
        if self.stimulation > 100:
            self.stimulation = 100

    def pet(self, person=None):
        # TODO increase relationship with person petting horse
        # from backend.time import time
        # time.pass_time(5)
        self.stimulation += 10
        if self.stimulation > 100:
            self.stimulation = 100

    def _get_limit(self, n):
        if n >= 76:
            return 75
        elif n >= 51:
            return 50
        elif n >= 26:
            return 25
        elif n >= 1:
            return 0
        else:
            return -1

    def _eat(self):
        items = self.stable.items
        for item in items:
            if item.name == "food" and self.location == "Stable":
                to_eat = 100 - self.food
                if item.value < to_eat:
                    self.food += item.value
                    item.value = 0
                else:
                    item.value -= to_eat
                    self.food = 100

        return self._get_limit(self.food)

    def _ch_food(self, now):
        """Calculates what the food meter should be at now,
        update the current value (and last updated field) and
        returns the timestamp for the next event."""
        last_updated = TimeStamp(self.food_date, self.food_time)
        time_passed = now - last_updated

        food_decay_time = 10
        self.food -= time_passed.get_min() / float(food_decay_time)
        self.food_date = now.date
        self.food_time = now.time

        t_next = copy.copy(now)
        if self.food >= 80:
            # No need to eat right now
            next_limit = 75
        elif self.food >= 1:
            next_limit = self._eat()
        else:
            # Food dropped to zero or below. Figure out what to do here.
            t_next.add_min(1440)
            return {"subject": "food", "t_stamp": t_next}

        t_next.add_min((self.food - next_limit) * food_decay_time)
        return {"subject": "food", "t_stamp": t_next}

    def _drink(self):
        items = self.stable.items
        for item in items:
            if item.name == "auto-water":
                self.water = 100
            elif item.name == "water":
                to_drink = 100 - self.water
                if item.value < to_drink:
                    self.water += item.value
                    item.value = 0
                else:
                    item.value -= to_drink
                    self.water = 100
        return self._get_limit(self.water)

    def _ch_water(self, now):
        last_updated = TimeStamp(self.water_date, self.water_time)
        time_passed = now - last_updated

        water_decay_time = 5
        self.water -= time_passed.get_min() / float(water_decay_time)
        self.water_date = now.date
        self.water_time = now.time

        t_next = copy.copy(now)
        if self.water >= 80:
            # No need to drink
            next_limit = 75
        elif self.water >= 1:
            next_limit = self._drink()
        else:
            t_next.add_min(1440)
            return {"subject": "water", "t_stamp": t_next}

        t_next.add_min((self.water - next_limit) * water_decay_time)
        return {"subject": "water", "t_stamp": t_next}

    def _ch_energy(self, now, night=False):
        last_updated = TimeStamp(self.energy_date, self.energy_time)
        time_passed = now - last_updated

        energy_inc_time = 3
        energy_decay_time = 20

        if night:
            self.energy += time_passed.get_min() / float(energy_inc_time)
        else:
            self.energy -= time_passed.get_min() / float(energy_decay_time)
        self.energy_date = now.date
        self.energy_time = now.time

        t_next = copy.copy(now)
        # Just check every two hours or so (small offset to prevent
        # everything from happening in the same minute).
        t_next.add_min(124)
        return {"subject": "energy", "t_stamp": t_next}

    def _ch_stimulation(self, now, night=False):
        last_updated = TimeStamp(self.stimulation_date,
                                 self.stimulation_time)
        time_passed = now - last_updated

        stimulation_decay_time = 1
        self.stimulation -= (time_passed.get_min() /
                             float(stimulation_decay_time))
        self.stimulation_date = now.date
        self.stimulation_time = now.time

        t_next = copy.copy(now)
        next_limit = self._get_limit(self.stimulation)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "stimulation", "t_stamp": t_next}

        t_next.add_min((self.stimulation - next_limit) *
                       stimulation_decay_time)
        return {"subject": "stimulation", "t_stamp": t_next}

    def _ch_social(self, now):
        last_updated = TimeStamp(self.social_date, self.social_time)
        time_passed = now - last_updated

        social_decay_time = 20
        self.social -= time_passed.get_min() / float(social_decay_time)
        self.social_date = now.date
        self.social_time = now.time

        t_next = copy.copy(now)
        next_limit = self._get_limit(self.social)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "social", "t_stamp": t_next}

        t_next.add_min((self.social - next_limit) * social_decay_time)
        return {"subject": "social", "t_stamp": t_next}

    def _ch_exercise(self, now):
        last_updated = TimeStamp(self.exercise_date, self.exercise_time)
        time_passed = now - last_updated

        exercise_decay_time = 10
        self.exercise -= time_passed.get_min() / float(exercise_decay_time)
        self.exercise_date = now.date
        self.exercise_time = now.time

        t_next = copy.copy(now)
        next_limit = self._get_limit(self.exercise)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "exercise", "t_stamp": t_next}

        t_next.add_min((self.exercise - next_limit) * exercise_decay_time)
        return {"subject": "exercise", "t_stamp": t_next}

    def _ch_hygiene(self, now):
        last_updated = TimeStamp(self.hygiene_date, self.hygiene_time)
        time_passed = now - last_updated

        hygiene_decay_time = 15
        self.hygiene -= time_passed.get_min() / float(hygiene_decay_time)
        self.hygiene_date = now.date
        self.hygiene_time = now.time

        t_next = copy.copy(now)
        next_limit = self._get_limit(self.hygiene)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "hygiene", "t_stamp": t_next}

        t_next.add_min((self.hygiene - next_limit) * hygiene_decay_time)
        return {"subject": "hygiene", "t_stamp": t_next}

    def get_events(self, now):
        events = []

        events.append(self._ch_food(now))
        events.append(self._ch_water(now))
        events.append(self._ch_energy(now))
        events.append(self._ch_stimulation(now))
        events.append(self._ch_social(now))
        events.append(self._ch_exercise(now))
        events.append(self._ch_hygiene(now))

        return events

    def event(self, subject, t_stamp, night=False):
        if subject == "food":
            e_info = self._ch_food(t_stamp)
        elif subject == "water":
            e_info = self._ch_water(t_stamp)
        elif subject == "energy":
            e_info = self._ch_energy(t_stamp, night)
        elif subject == "stimulation":
            e_info = self._ch_stimulation(t_stamp, night)
        elif subject == "social":
            e_info = self._ch_social(t_stamp)
        elif subject == "exercise":
            e_info = self._ch_exercise(t_stamp)
        elif subject == "hygiene":
            e_info = self._ch_hygiene(t_stamp)

        return e_info

    def __str__(self):
        return self.name

    def get(self, now, key):
        if key == "food":
            e_info = self._ch_food(now)
            result = self.food
        elif key == "water":
            e_info = self._ch_water(now)
            result = self.water
        elif key == "energy":
            e_info = self._ch_energy(now)
            result = self.energy
        elif key == "stimulation":
            e_info = self._ch_stimulation(now)
            result = self.stimulation
        elif key == "social":
            e_info = self._ch_social(now)
            result = self.social
        elif key == "exercise":
            e_info = self._ch_exercise(now)
            result = self.exercise
        elif key == "hygiene":
            e_info = self._ch_hygiene(now)
            result = self.hygiene
        else:
            e_info = None
            result = getattr(self, key)
        return {"attr": result, "e_info": e_info}
