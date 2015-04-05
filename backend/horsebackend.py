from backend import Backend
from models.horse import Horse


class HorsesBackend(Backend):
    @classmethod
    def all(cls, session):
        return session.query(Horse).order_by(Horse.id)

    @classmethod
    def one(cls, session, id):
        return session.query(Horse).filter_by(id=id)[0]
