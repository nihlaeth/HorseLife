from backend import Backend
from session import session_scope
from models.horse import Horse


class HorsesBackend(Backend):
    @classmethod
    def all(cls):
        with session_scope() as session:
            return session.query(Horse).order_by(Horse.id)

    @classmethod
    def one(cls, id):
        with session_scope() as session:
            return session.query(Horse).filter_by(Horse.id == id)
