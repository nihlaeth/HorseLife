"""Provide abstraction layer for Horse model."""
from backend import Backend
from level import Level
from models.horse import Horse


class HorseBackend(Backend):

    """Abstraction layer for Horse model."""

    @classmethod
    def all_raw(cls, session):
        """Return all the raw horse instances."""
        return session.query(Horse)

    @classmethod
    def all(cls, session):
        """Return a list of all the horses in the db (encapsulated).

        session -- sqlalchemy session
        """
        horses = session.query(Horse).order_by(Horse.mid)
        return [HorseBackend(session, horse.mid) for horse in horses]

    @classmethod
    def _one_id(cls, session, id_):
        """Return (unencapsulated) horse model - for internal use only.

        session -- sqlalchemy session
        id -- id of horse model (int)
        """
        return session.query(Horse).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Backend sets self.id_, self._cls is for inherited methods."""
        Backend.__init__(self, session, id_)
        self._cls = "HorseBackend"

    def groom(self, session, now):
        """Groom encapsulated horse and return the current time.

        session -- sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating time at the end of this action
        """
        horse = self._one_id(session, self.id_)
        result = horse.groom(now)
        self._update_event(session, result["e_stimulation"])
        self._update_event(session, result["e_hygiene"])
        if self._level is None:
            self._level = Level(session)
        self._level.add_xp(session, now, 5)
        return result["clock"]  # Let core deal with timekeeping

    def pet(self, session, now):
        """Pet encapsulated horse and return current time.

        session --sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating time at the end of this action
        """
        horse = self._one_id(session, self.id_)
        result = horse.pet(now)
        self._update_event(session, result["e_info"])
        if self._level is None:
            self._level = Level(session)
        self._level.add_xp(session, now, 1)
        return result["clock"]
