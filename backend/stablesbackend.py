from backend import Backend
from session import session_scope
from models.stable import Stable

class StablesBackend(Backend):
    @classmethod
    def all(cls):
        with session_scope() as session:
            return session.query(Stable).order_by(Stable.name)

    @classmethod
    def one(cls, id):
        with session_scope() as session:
            return session.query(Stable).filter_by(Stable.id==id)
