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
        hygiene_decay_time = 15
        social_decay_time = 20
        energy_increase_time = 3
        exercise_decay_time = 10
        stimulation_decay_time = 1

        self.food -= minutes / float(food_decay_time)
        self.water -= minutes / float(water_decay_time)
        self.hygiene -= minutes / float(hygiene_decay_time)
        self.social -= minutes / float(social_decay_time)
        self.exercise -= minutes / float(exercise_decay_time)

        if night and self.location == "Stable":
            self.energy += minutes / float(energy_increase_time)

        items = self.stable.items
        if not night and self.location == "Stable":
            # Horses get bored when they're
            # penned up all day. If they have
            # a toy, or another horse nearby,
            # or, for example, room to run around,
            # they're much happier.
            toy = False
            for item in items:
                if item.name == "toy":
                    toy = True
            if not toy and len(self.stable.horses) < 2:
                # TODO check if other horse is actually in stable
                self.stimulation -= minutes / float(stimulation_decay_time)
            else:
                # There is something to stimulate the horse!
                # Increase stimulation.
                self.stimulation += minutes / float(stimulation_decay_time)
        if self.food < 75 and self.location == "Stable":
            # Try to eat.
            for item in items:
                if item.name == "food":
                    to_eat = 100 - self.food
                    if item.value < to_eat:
                        self.food += item.value
                        item.value = 0
                    else:
                        item.value -= to_eat
                        self.food = 100
        if self.water < 75 and self.location == "Stable":
            # Try to drink.
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
        if self.exercise < 0:
            self.exercise = 0
        if self.stimulation > 100:
            self.stimulation = 100
        if self.stimulation < 0:
            self.stimulation = 0
        # TODO exercise need is dependent on a couple of things
        # TODO update health as some needs drop too low
        # TODO update happiness according to needs

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
        if self.food >= 76:
            return 75
        if self.food >= 51:
            return 50
        if self.food >= 26:
            return 25
        return 0

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

        if self.food >= 80:
            # No need to eat right now
            next_limit = 75
        elif self.food >= 1:
            next_limit = self._eat()
        else:
            # Food dropped to zero or below. Figure out what to do here.
            now.add_min(14)
            return ["food", now]

        now.add_min((self.food - next_limit) * food_decay_time)
        return ["food", now]

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
        if self.water >= 76:
            return 75
        if self.water >= 51:
            return 50
        if self.water >= 26:
            return 25
        return 0

    def _ch_water(self, now):
        last_updated = TimeStamp(self.water_date, self.water_time)
        time_passed = now - last_updated

        water_decay_time = 5
        self.water -= time_passed.get_min() / float(water_decay_time)
        self.water_date = now.date
        self.water_time = now.time

        if self.water >= 80:
            # No need to drink
            next_limit = 75
        elif self.water >= 1:
            next_limit = self._drink()
        else:
            now.add_min(16)
            return ["water", now]

        now.add_min((self.water - next_limit) * water_decay_time)
        return ["water", now]

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

        # Just check every two hours or so (small offset to prevent
        # everything from happening in the same minute).
        now.add_min(124)
        return ["energy", now]

    def get_events(self, now):
        events = []

        # For every need, calculate when the next event takes place.
        events.append(self._ch_food(now))
        events.append(self._ch_water(now))
        events.append(self._ch_energy(now))

        return events

    def event(self, event):
        if event.subject == "food":
            next_event = self._ch_water(event.t_stamp)
        elif event.subject == "water":
            next_event = self._ch_water(event.t_stamp)
        elif event.subject == "energy":
            next_event = self._ch_energy(event.t_stamp, event.night)

        return next_event

    def __str__(self):
        return self.name

    def get(self, now, key):
        if key == "food":
            self._ch_food(now)
            return self.food
        elif key == "water":
            self._ch_water(now)
            return self.water
        elif key == "energy":
            self._ch_energy(now)
            return self.energy
        else:
            return getattr(self, key)
