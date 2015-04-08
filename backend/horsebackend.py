from backend import Backend
from models.horse import Horse


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

    def get(self, session, name):
        horse = self._one_id(session, self._id)
        return getattr(horse, name)

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
