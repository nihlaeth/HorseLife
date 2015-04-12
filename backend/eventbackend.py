from backend import Backend
from models.event import Event


class EventBackend(Backend):
    @classmethod
    def all(cls, session):
        models = session.query(Event).order_by(Event.date, Event.time)
        return [EventBackend(model.id) for model in models]

    @classmethod
    def one(cls, session, subject, obj_id):
        return EventBackend(
                session.query(Event).filter(
                    Event.subject == subject,
                    Event.obj_id == obj_id)[0].id)

    @classmethod
    def next_event(cls, session):
        return EventBackend(
                session.query(Event).order_by(Event.date, Event.time)[0].id)

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Event).filter_by(id=id)[0]

    def __init__(self, id):
        self._id = id

    def get(self, session, name):
        event = EventBackend._one_id(session, self._id)
        return getattr(event, name)

    def set(self, session, name, value):
        event = EventBackend._one_id(session, self._id)
        setattr(event, name, value)

    def update(self, session, timestamp):
        event = EventBackend._one_id(session, self._id)
        event.update(timestamp)

    def string(self, session):
        event = EventBackend._one_id(session, self._id)
        print str(event)
