from backend import Backend
from models.horse import Horse
from eventbackend import EventBackend
from generators.eventgenerator import EventGenerator


class HorseBackend(Backend):
    @classmethod
    def all_raw(cls, session):
        """ Return all the raw horse instances."""
        return session.query(Horse)

    @classmethod
    def all(cls, session):
        """ Return a list of all the horses in the db (encapsulated).

        session -- sqlalchemy session
        """
        horses = session.query(Horse).order_by(Horse.id)
        return [HorseBackend(horse.id) for horse in horses]

    @classmethod
    def _one_id(cls, session, id):
        """ Return (unencapsulated) horse model - for internal use only!

        session -- sqlalchemy session
        id -- id of horse model (int)"""
        return session.query(Horse).filter_by(id=id)[0]

    def __init__(self, id):
        """ Backend sets self._id, self._str is for inherited methods."""
        Backend.__init__(self, id)
        self._str = "HorseBackend"

    def groom(self, session, now):
        """ Groom encapsulated horse and return the current time.

        session -- sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating time at the end of this action
        """
        horse = self._one_id(session, self._id)
        result = horse.groom(now)
        self._update_event(session, result["e_stimulation"])
        self._update_event(session, result["e_hygiene"])
        return result["clock"]  # Let core deal with timekeeping

    def pet(self, session, now):
        """ Pet encapsulated horse and return current time.

        session --sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating time at the end of this action
        """
        horse = self._one_id(session, self._id)
        result = horse.pet(now)
        self._update_event(session, result["e_info"])
        return result["clock"]
