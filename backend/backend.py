from eventbackend import EventBackend
from generators.eventgenerator import EventGenerator


class Backend():
    @classmethod
    def one(cls, id):
        pass

    @classmethod
    def all(cls):
        pass

    def __init__(self, id):
        self._id = id
        self._str = "Backend"

    def get(self, session, t_stamp, key):
        instance = self._one_id(session, self._id)
        info = instance.get(t_stamp, key)
        if info["e_info"] is not None:
            self._update_event(session, info["e_info"])
        return info["attr"]

    def set(self, session, name, value):
        instance = self._one_id(session, self._id)
        setattr(instance, name, value)

    def get_events(self, session, now):
        instance = self._one_id(session, self._id)

        events = {}
        result = instance.get_events(now)
        for e_info in result:
            if e_info is not None:
                events[e_info["subject"]] = {
                        "obj_id": self._id,
                        "date": e_info["t_stamp"].date,
                        "time": e_info["t_stamp"].time,
                        "callbacks": [[self._str, self._id]]}
        EventGenerator.gen_many(session, events)

    def _update_event(self, session, e_info):
        event = EventBackend.one(session, e_info["subject"], self._id)
        event.update(session, e_info["t_stamp"])

    def event_callback(self, session, subject, t_stamp):
        instance = self._one_id(session, self._id)
        e_info = instance.event(subject, t_stamp)
        self._update_event(session, e_info)
