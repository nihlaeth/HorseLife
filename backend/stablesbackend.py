from backend import Backend
from models.stable import Stable


class StablesBackend(Backend):
    @classmethod
    def all(cls, session):
        stables = session.query(Stable).order_by(Stable.name)
        return [StablesBackend(stable.id) for stable in stables]

    @classmethod
    def one(cls, session, id):
        # This method is here for consistency's sake.
        return StablesBackend(id)

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
