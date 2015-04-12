from backend import Backend
from eventbackend import EventBackend
from models.stable import Stable
from generators.eventgenerator import EventGenerator


class StableBackend(Backend):
    @classmethod
    def all(cls, session):
        stables = session.query(Stable).order_by(Stable.name)
        return [StableBackend(stable.id) for stable in stables]

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Stable).filter_by(id=id)[0]

    def __init__(self, id):
        self._id = id

    def get(self, session, t_stamp, key):
        stable = self._one_id(session, self._id)
        info = stable.get(t_stamp, key)
        if info["e_info"] is not None:
            self._update_event(session, info["e_info"])
        return info["attr"]

    def set(self, session, name, value):
        stable = self._one_id(session, self._id)
        setattr(stable, name, value)

    def clean(self, session, now):
        stable = self._one_id(session, self._id)
        result = stable.clean(now)
        self._update_event(session, result["e_info"])
        return result["clock"]

    def food(self, session):
        stable = self._one_id(session, self._id)
        return stable.food()

    def water(self, session):
        stable = self._one_id(session, self._id)
        return stable.water()

    def __repr__(self):
        # TODO find elegant way to get repr info
        # without a session - and have the info not
        # be stale.
        return "Stable -- no session == no info"

    def __str__(self):
        # TODO same as above
        return "Stable -- no session == no info"

    def get_events(self, session, now):
        stable = self._one_id(session, self._id)

        events = {}
        result = stable.get_events(now)
        for e_info in result:
            if e_info is not None:
                events[e_info["subject"]] = [
                        self._id,
                        e_info["t_stamp"].date,
                        e_info["t_stamp"].time,
                        [["StableBackend", self._id]]]
        EventGenerator.gen_many(session, events)

    def _update_event(self, session, e_info):
        event = EventBackend.one(session, e_info["subject"], self._id)
        event.update(session, e_info["t_stamp"])

    def event_callback(self, session, subject, t_stamp):
        stable = self._one_id(session, self._id)
        e_info = stable.event(subject, t_stamp)
        self._update_event(session, e_info)
