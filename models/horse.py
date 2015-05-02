"""Horse model."""
import copy
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean

from base import BASE
from support.messages.timestamp import TimeStamp


# Sqlalchemy handles the __init__, the instance attributes
# is a case of wontfix. The code won't get any better if we split
# some off into their own models.
# pylint: disable=no-init,too-many-instance-attributes
class Horse(BASE):

    """Represents a horse."""

    __tablename__ = 'horses'

    mid = Column(Integer, primary_key=True)

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
    stimulation_msg = Column(Boolean)

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

    stable_id = Column(Integer, ForeignKey('stables.mid'))
    owner_id = Column(Integer, ForeignKey('people.mid'))

    def groom(self, now, skill="normal"):
        """Groom the horse (clean, brush).

        It takes about 30 minutes.
        In the future, skill will play a role here.
        """
        # Grooming takes about 30 minutes, so update the timestamp.
        now.add_min(30)

        # First, make sure the stimulation and hygiene stats are
        # updated:
        self._ch_stimulation(now)
        self._ch_hygiene(now)

        # Now make the changes we want
        self.stimulation += 40
        self.hygiene = 100
        if self.stimulation > 100:
            self.stimulation = 100

        # Now get the updated event information to pass on:
        e_info_stimulation = self._ch_stimulation(now)
        e_info_hygiene = self._ch_hygiene(now)

        return {"clock": now,
                "e_stimulation": e_info_stimulation,
                "e_hygiene": e_info_hygiene}

    def pet(self, now, person=None):
        """Pet horse, takes about 5 minutes and stimulates the horse.

        In the future, this will effect the relationship between player
        and horse.
        """
        now.add_min(5)

        self._ch_stimulation(now)

        self.stimulation += 10
        if self.stimulation > 100:
            self.stimulation = 100

        e_info = self._ch_stimulation(now)
        return {"clock": now, "e_info": e_info}

    # TODO fix duplication - move to common parent
    def _get_limit(self, num):
        """Determine where the next event border is.

        Helper method for the _ch_* methods.

        num -- current need value
        This function determines where the next event border is.
        """
        if num >= 26:
            return 25
        elif num >= 1:
            return 0
        else:
            return -1

    def _eat(self):
        """Have the horse eat.

        This is something it does independently
        of the player.

        In the future, different food types will sustain the horse for
        different times / levels of activity.
        """
        # stable is an attribute created by sqlalchemy (backref)
        # pylint: disable=no-member
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
        """Calculate what the food meter should be at now."""
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
            return {"subject": "food", "t_stamp": t_next, "msg": None}

        t_next.add_min((self.food - next_limit) * food_decay_time)
        return {"subject": "food", "t_stamp": t_next, "msg": None}

    def _drink(self):
        """Have the horse drink.

        This is done independently from the player.
        """
        # stable is provided by sqlalchemy (backref)
        # pylint: disable=no-member
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
        """Calculate current value of water meter."""
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
            return {"subject": "water", "t_stamp": t_next, "msg": None}

        t_next.add_min((self.water - next_limit) * water_decay_time)
        return {"subject": "water", "t_stamp": t_next, "msg": None}

    def _ch_energy(self, now):
        """Calculate current value of energy meter."""
        night = now.is_night()
        last_updated = TimeStamp(self.energy_date, self.energy_time)
        time_passed = now - last_updated

        energy_inc_time = 3
        energy_decay_time = 20

        if night:
            self.energy += time_passed.get_min() / float(energy_inc_time)
        else:
            self.energy -= time_passed.get_min() / float(energy_decay_time)
        # Make sure energy stays within reasonable limits.
        if self.energy > 100:
            self.energy = 100
        elif self.energy < 0:
            self.energy = 0

        self.energy_date = now.date
        self.energy_time = now.time

        t_next = copy.copy(now)
        if night:
            # If it's night, we want to have an event at the end of
            # it, to make sure the energy level raises correctly.
            t_next.end_of_night(event=True)
        else:
            # Make sure horse loses energy until it's night
            t_next.start_of_night(event=True)
        return {"subject": "energy", "t_stamp": t_next, "msg": None}

    def _ch_stimulation(self, now):
        """Calculate current value of stimulation meter."""
        night = now.is_night()
        last_updated = TimeStamp(self.stimulation_date,
                                 self.stimulation_time)
        time_passed = now - last_updated

        stimulation_decay_time = 1
        # Stimulation only decays if the horse is awake.
        if not night:
            self.stimulation -= (time_passed.get_min() /
                                 float(stimulation_decay_time))
        self.stimulation_date = now.date
        self.stimulation_time = now.time
        # Make sure stimulation stays within reasonable limits
        if self.stimulation < 0:
            self.stimulation = 0
        elif self.stimulation > 100:
            # This method can't raise it above a hundred, but some other
            # method might.
            self.stimulation = 100

        # See if there's a message to be delivered
        if self.stimulation < 25 and not self.stimulation_msg:
            msg = {
                "subject": "%s is getting bored!" % self.name,
                "t_stamp": now,
                "text": (
                    "Bored horses can develop bad habits, "
                    "like weaving for example. But more "
                    "importantly, they get unhappy when "
                    "they're bored. So go entertain %s!"
                    " You could also get them a toy to "
                    "keep them entertained, or better yet, "
                    "a stablemate. Some time in the pasture "
                    "will also do them good. Good luck!" % self.name)}
            self.stimulation_msg = True
        else:
            msg = None
            if self.stimulation >= 25:
                # Stimulation is at healthy levels, reset msg attribute.
                self.stimulation_msg = False
        t_next = copy.copy(now)
        next_limit = self._get_limit(self.stimulation)
        if next_limit < 0:
            t_next.add_min(1440)
            return {"subject": "stimulation", "t_stamp": t_next, "msg": msg}

        t_next.add_min((self.stimulation - next_limit) *
                       stimulation_decay_time)
        if t_next.is_night() != night:
            # Passed a day/night change, put the next event at
            # the exact change to ensure correct energy decay.
            # Reset t_next
            t_next = copy.copy(now)
            if night:
                t_next.end_of_night(event=True)
            else:
                t_next.start_of_night(event=True)

        return {"subject": "stimulation", "t_stamp": t_next, "msg": msg}

    def _ch_social(self, now):
        """Calculate current value of social meter."""
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
            return {"subject": "social", "t_stamp": t_next, "msg": None}

        t_next.add_min((self.social - next_limit) * social_decay_time)
        return {"subject": "social", "t_stamp": t_next, "msg": None}

    def _ch_exercise(self, now):
        """Calculate current value of exercise meter."""
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
            return {"subject": "exercise", "t_stamp": t_next, "msg": None}

        t_next.add_min((self.exercise - next_limit) * exercise_decay_time)
        return {"subject": "exercise", "t_stamp": t_next, "msg": None}

    def _ch_hygiene(self, now):
        """Calculate current value of hygiene meter."""
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
            return {"subject": "hygiene", "t_stamp": t_next, "msg": None}

        t_next.add_min((self.hygiene - next_limit) * hygiene_decay_time)
        return {"subject": "hygiene", "t_stamp": t_next, "msg": None}

    def _update_environment(self, now):
        """Set environment.

        This has a different name than the _ch methods, as it has no
        associated event.
        """
        # stable is dynamically generated by sqlalchemy.
        # pylint: disable=no-member
        stable = self.stable

        # Environment depends on a number of factors:
        # cleanliness of stable
        # presence of distraction in the form of toys or outside space
        # amount of light
        # size of stable divided by number of horses in said stable

        # Minimum surface per horse is 9 right now, that shoult translate
        # to zero environment score for size (max 25).
        # A large stable is 16 m2 right now, that should translate to
        # a maximum score of 25. Anything above that (a stable that's not
        # filled to capacity for example), should still translate to 25.
        size_score = (stable.surface / len(stable.horses) - 9) * 25/7.
        if size_score > 25:
            size_score = 25
        # TODO: have size of horse breed factor into environment
        # Large horses are not well suited for small stables.

        # cleanliness has a value between 0 and 100, so dividing it by
        # 4 should give us a scale between 0 and 25.
        cleanliness_info = stable.get(now, "cleanliness")
        cleanliness_score = cleanliness_info["attr"] / 4.

        # light also has a value between 0 and 100, so dividing by 4
        # does the trick.
        light_score = stable.light / 4.

        # stimulation score is more difficult to calculate, as it depends
        # on a number of things in and of itself. For now, toys haven't
        # been implemented yet, so we can't check for them, but we do
        # factor them into the equasion (or we'll get a lot of failing
        # tests when we do implement them).
        #
        # Let's treat this as a scale from 0 to 100. Having a pasture
        # with the stable counts for 50 points. How much doesn't really
        # matter. Having other horses to socialize with counts for 30,
        # and the presence of toys makes the remaining 20 points.
        stimulation_score = 0
        stimulation_score += 50 if stable.outside_surface > 0 else 0
        stimulation_score += 30 if len(stable.horses) > 1 else 0
        # TODO: check if horse actually likes the other horse(s) in the
        # stable.
        stimulation_score += 0  # TODO: check for toys
        stimulation_score /= 4.

        self.environment = (
            size_score +
            cleanliness_score +
            light_score +
            stimulation_score)
        return cleanliness_info["e_info"]

    def _update_happiness(self, now):
        """Calculate happiness value.

        Problem: happiness depends on time dependent needs - we should
        make sure they're up to date, only I fear the performance
        implications.
        """
        # As there are 5 dependencies, every one of them should be
        # on a scale of 0 to 20.
        result = []
        result.append(self._ch_exercise(now))
        exercise_score = self.exercise / 5.

        result.append(self._ch_hygiene(now))
        hygiene_score = self.hygiene / 5.

        result.append(self._ch_stimulation(now))
        stimulation_score = self.stimulation / 5.

        result.append(self._update_environment(now)[0])
        environment_score = self.environment / 5.

        result.append(self._ch_social(now))
        social_score = self.social / 5.

        self.happiness = (
            exercise_score +
            hygiene_score +
            stimulation_score +
            environment_score +
            social_score)

        # food and water are primal needs, they influence the entire
        # happiness scale.
        result.append(self._ch_food(now))
        result.append(self._ch_water(now))
        if self.food < 10 or self.water < 10:
            self.happiness = 0
        elif self.food < 30 or self.water < 30:
            self.happiness /= 4.

        return result

    def get_events(self, now):
        """Get a single event for every need meter and return event info."""
        events = []

        events.append(self._ch_food(now))
        events.append(self._ch_water(now))
        events.append(self._ch_energy(now))
        events.append(self._ch_stimulation(now))
        events.append(self._ch_social(now))
        events.append(self._ch_exercise(now))
        events.append(self._ch_hygiene(now))

        return events

    def event(self, subject, t_stamp):
        """Handle event, is called at event activation."""
        if subject == "food":
            e_info = self._ch_food(t_stamp)
        elif subject == "water":
            e_info = self._ch_water(t_stamp)
        elif subject == "energy":
            e_info = self._ch_energy(t_stamp)
        elif subject == "stimulation":
            e_info = self._ch_stimulation(t_stamp)
        elif subject == "social":
            e_info = self._ch_social(t_stamp)
        elif subject == "exercise":
            e_info = self._ch_exercise(t_stamp)
        elif subject == "hygiene":
            e_info = self._ch_hygiene(t_stamp)

        return e_info

    def __str__(self):
        """Return string representation of object."""
        return self.name

    def get(self, now, key):
        """Get an attribute.

        If it's an active stat (need), it will
        be calculated / updated to current timestamp first. Aside from
        the attribute value, this also returns the info needed to update
        the event in question.
        """
        if key == "food":
            e_info = [self._ch_food(now)]
            result = self.food
        elif key == "water":
            e_info = [self._ch_water(now)]
            result = self.water
        elif key == "energy":
            e_info = [self._ch_energy(now)]
            result = self.energy
        elif key == "stimulation":
            e_info = [self._ch_stimulation(now)]
            result = self.stimulation
        elif key == "social":
            e_info = [self._ch_social(now)]
            result = self.social
        elif key == "exercise":
            e_info = [self._ch_exercise(now)]
            result = self.exercise
        elif key == "hygiene":
            e_info = [self._ch_hygiene(now)]
            result = self.hygiene
        elif key == "environment":
            e_info = self._update_environment(now)
            result = self.environment
        elif key == "happiness":
            e_info = self._update_happiness(now)
            result = self.happiness
        else:
            e_info = None
            result = getattr(self, key)
        return {"attr": result, "e_info": e_info}
