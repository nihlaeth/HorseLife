from backend import Backend
from time import time
from models.horse import Horse
from support.messages.event import Event


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

    def get(self, session, key):
        now = time.get_time_stamp(session)
        horse = self._one_id(session, self._id)
        return horse.get(now, key)

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

        events = []
        result = horse.get_events(now)
        for e in result:
            if e is not None:
                events.append(Event(
                    e[1].date,
                    e[1].time,
                    self.event_callback,
                    e[0]))

        time.add_event_multi(events)

    def event_callback(self, session, event):
        """Execute event, and place the returned next occurence
        in the event queue."""
        horse = self._one_id(session, self._id)
        event_list = horse.event(event)
        if event_list is not None:
            next_event = Event(
                event_list[1].date,
                event_list[1].time,
                self.event_callback,
                event_list[0])
            time.add_event(next_event)
