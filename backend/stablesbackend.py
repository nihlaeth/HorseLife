from backend import Backend
from models.stable import Stable


class StablesBackend(Backend):
    @classmethod
    def all(cls, session):
        return session.query(Stable).order_by(Stable.name)

    @classmethod
    def one(cls, session, id):
        return session.query(Stable).filter_by(id=id)[0]
