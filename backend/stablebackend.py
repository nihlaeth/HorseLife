from backend import Backend
from models.stable import Stable


class StableBackend(Backend):
    @classmethod
    def all(cls, session):
        stables = session.query(Stable).order_by(Stable.name)
        return [StableBackend(stable.id) for stable in stables]

    @classmethod
    def one(cls, session, id):
        # This method is here for consistency's sake.
        return StableBackend(id)

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Stable).filter_by(id=id)[0]

    def __init__(self, id):
        self._id = id

    def get(self, session, name):
        stable = self._one_id(session, self._id)
        return getattr(stable, name)

    def set(self, session, name, value):
        stable = self._one_id(session, self._id)
        setattr(stable, name, value)

    def pass_time(self, session, minutes, night):
        stable = self._one_id(session, self._id)
        return stable.pass_time(minutes, night)

    def clean(self, session):
        stable = self._one_id(session, self._id)
        return stable.clean()

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
        return ""

    def __str__(self):
        # TODO same as above
        return ""
