"""Provide abstraction layer for Pasture model."""
from backend import Backend
from level import Level
from models.pasture import Pasture


class PastureBackend(Backend):

    """Abstraction layer for Pasture."""

    @classmethod
    def all(cls, session):
        """Return a list of all encapsulated pasture models."""
        pastures = session.query(Pasture).order_by(Pasture.name)
        return [PastureBackend(session, pasture.mid) for pasture in pastures]

    @classmethod
    def all_raw(cls, session):
        """Return a list of raw pasture models."""
        return session.query(Pasture)

    @classmethod
    def _one_id(cls, session, id_):
        """Return bare pasture model - internal use only."""
        return session.query(Pasture).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Set some basics."""
        Backend.__init__(self, session, id_)
        self._cls = "PastureBackend"

    def clean(self, session, now):
        """Clean pasture."""
        pasture = self._one_id(session, self.id_)
        result = pasture.clean(now)
        self._update_event(session, result["e_info"])
        if self._level is None:
            self._level = Level(session)
        self._level.add_xp(session, now, 20)
        return result["clock"]

    def remove_horse(self, session, horse):
        """Remove horse from pasture.

        session -- sqlalchemy session
        horse -- HorseBackend object
        """
        pasture = self._one_id(session, self.id_)

        # we need to pass the raw horse model to the pasture
        horse_raw = horse.raw(session)

        pasture.remove_horse(horse_raw)
