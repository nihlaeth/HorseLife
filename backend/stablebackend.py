"""Provide abstraction layer for Stable model."""
from backend import Backend
from level import Level
from models.stable import Stable


class StableBackend(Backend):

    """Abstraction layer for Stable model."""

    @classmethod
    def all_raw(cls, session):
        """Return all raw instances of Stable."""
        return session.query(Stable)

    @classmethod
    def all(cls, session):
        """Return a list of all encapsulated stable models.

        session -- sqlalchemy session
        """
        stables = session.query(Stable).order_by(Stable.name)
        return [StableBackend(session, stable.mid) for stable in stables]

    @classmethod
    def _one_id(cls, session, id_):
        """Return bare stable model - internal use only.

        session -- sqlalchemy session
        id -- model id (int)
        """
        return session.query(Stable).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Backend sets _id, _cls is for use with inherited methods."""
        Backend.__init__(self, session, id_)
        self._cls = "StableBackend"

    def clean(self, session, now):
        """Execute clean method on encapsulated model.

        session -- sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating the time at the end of action
        """
        stable = self._one_id(session, self.id_)
        result = stable.clean(now)
        self._update_event(session, result["e_info"])
        if self._level is None:
            self._level = Level(session)
        self._level.add_xp(session, now, 5)
        return result["clock"]

    def food(self, session, now):
        """Add food to encapsulated stable.

        session -- sqlalchemy session

        Note: this does not take care of side effects like food supply,
        all it does is fill the feeding tray in this particular stable.
        In the future, we'll want to do something with types of food.
        """
        stable = self._one_id(session, self.id_)
        result = stable.food(now)
        if self._level is None:
            self._level = Level(session)
        self._level.add_xp(session, now, 1)
        return result["clock"]

    def water(self, session, now):
        """Provide water for encapsulated stable.

        session -- sqlalchemy
        """
        stable = self._one_id(session, self.id_)
        result = stable.water(now)
        if self._level is None:
            self._level = Level(session)
        self._level.add_xp(session, now, 1)
        return result["clock"]
