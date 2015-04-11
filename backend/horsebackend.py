from backend import Backend
from models.horse import Horse
from eventbackend import EventBackend
from generators.eventgenerator import EventGenerator


class HorseBackend(Backend):
    @classmethod
    def all(cls, session):
        horses = session.query(Horse).order_by(Horse.id)
        return [HorseBackend(horse.id) for horse in horses]

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Horse).filter_by(id=id)[0]

    def __init__(self, id):
        self._id = id

    def get(self, session, t_stamp, key):
        horse = self._one_id(session, self._id)
        return horse.get(t_stamp, key)

    def set(self, session, name, value):
        horse = self._one_id(session, self._id)
        setattr(horse, name, value)

    def pass_time(self, session, minutes, night):
        horse = self._one_id(session, self._id)
        horse.pass_time(minutes, night)

    def groom(self, session):
        horse = self._one_id(session, self._id)
        horse.groom()

    def pet(self, session):
        horse = self._one_id(session, self._id)
        horse.pet()

    def get_events(self, session, now):
        """Fetch events from model - one event for every
        type of occurence (need based)."""
        horse = self._one_id(session, self._id)

        events = {}
        result = horse.get_events(now)
        for e in result:
            if e is not None:
                events[e[0]] = [
                    e[1].date,
                    e[1].time,
                    [["HorseBackend", 1]]]
        EventGenerator.gen_many(session, events)

    def event_callback(self, session, subject, t_stamp):
        """Execute event, and update the event with next occurence
        time in the event queue."""
        horse = self._one_id(session, self._id)
        event_list = horse.event(subject, t_stamp)
        event = EventBackend.one(session, event_list[0])
        event.update(session, event_list[1])
