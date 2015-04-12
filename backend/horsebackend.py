from backend import Backend
from models.horse import Horse
from eventbackend import EventBackend
from generators.eventgenerator import EventGenerator


class HorseBackend(Backend):
    @classmethod
    def all(cls, session):
        horses = session.query(Horse).order_by(Horse.id)
        return [HorseBackend(horse.id) for horse in horses]

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Horse).filter_by(id=id)[0]

    def __init__(self, id):
        Backend.__init__(self, id)
        self._str = "HorseBackend"

    def groom(self, session, now):
        horse = self._one_id(session, self._id)
        result = horse.groom(now)
        self._update_event(session, result["e_stimulation"])
        self._update_event(session, result["e_hygiene"])
        return result["clock"]  # Let core deal with timekeeping

    def pet(self, session, now):
        horse = self._one_id(session, self._id)
        result = horse.pet(now)
        self._update_event(session, result["e_info"])
        return result["clock"]
