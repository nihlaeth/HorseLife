from backend import Backend
from session import session_scope
from models.building import Building

class BuildingsBackend(Backend):
    @classmethod
    def all(cls):
        with session_scope() as session:
            return session.query(Building).order_by(Building.location)

    @classmethod
    def one(cls, id):
        with session_scope() as session:
            return session.query(Building).filter_by(Building.id==id)
