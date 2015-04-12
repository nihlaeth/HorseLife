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
        Backend.__init__(self, id)
        self._str = "StableBackend"

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
