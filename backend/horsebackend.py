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
        info = horse.get(t_stamp, key)
        if info["e_info"] is not None:
            self._update_event(session, info["e_info"])
        return info["attr"]

    def set(self, session, name, value):
        horse = self._one_id(session, self._id)
        setattr(horse, name, value)

    def groom(self, session, now):
        horse = self._one_id(session, self._id)
        result = horse.groom(now)
        self._update_event(session, result["e_stimulation"])
        self._update_event(session, result["e_hygiene"])
        return result["clock"]  # Let core deal with timekeeping

    def pet(self, session, now):
        horse = self._one_id(session, self._id)
        result = horse.pet(now)
        self._update_event(session, result["e_info"])
        return result["clock"]

    def get_events(self, session, now):
        """Fetch events from model - one event for every
        type of occurence (need based)."""
        horse = self._one_id(session, self._id)

        events = {}
        result = horse.get_events(now)
        for e_info in result:
            if e_info is not None:
                events[e_info["subject"]] = [
                    self._id,
                    e_info["t_stamp"].date,
                    e_info["t_stamp"].time,
                    [["HorseBackend", self._id]]]
        EventGenerator.gen_many(session, events)

    def _update_event(self, session, e_info):
        event = EventBackend.one(session, e_info["subject"], self._id)
        event.update(session, e_info["t_stamp"])

    def event_callback(self, session, subject, t_stamp):
        """Execute event, and update the event with next occurence
        time in the event queue."""
        horse = self._one_id(session, self._id)
        e_info = horse.event(subject, t_stamp)
        self._update_event(session, e_info)
