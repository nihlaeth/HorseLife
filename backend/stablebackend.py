"""Provide abstraction layer for Stable model."""
from backend import Backend
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
        return [StableBackend(stable.mid) for stable in stables]

    @classmethod
    def _one_id(cls, session, id_):
        """Return bare stable model - internal use only.

        session -- sqlalchemy session
        id -- model id (int)
        """
        return session.query(Stable).filter_by(mid=id_)[0]

    def __init__(self, id_):
        """Backend sets _id, _str is for use with inherited methods."""
        Backend.__init__(self, id_)
        self._str = "StableBackend"

    def clean(self, session, now):
        """Execute clean method on encapsulated model.

        session -- sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating the time at the end of action
        """
        stable = self._one_id(session, self.id_)
        result = stable.clean(now)
        self._update_event(session, result["e_info"])
        return result["clock"]

    def food(self, session):
        """Add food to encapsulated stable.

        session -- sqlalchemy session

        Note: this does not take care of side effects like food supply,
        all it does is fill the feeding tray in this particular stable.
        In the future, we'll want to do something with types of food.
        """
        stable = self._one_id(session, self.id_)
        return stable.food()

    def water(self, session):
        """Provide water for encapsulated stable.

        session -- sqlalchemy
        """
        stable = self._one_id(session, self.id_)
        return stable.water()

    def __repr__(self):
        """Return string representation of encapsulated model."""
        # TODO find elegant way to get repr info
        # without a session - and have the info not
        # be stale.
        return "Stable -- no session == no info"

    def __str__(self):
        """Return string representation of encapsulated model."""
        # TODO same as above
        return "Stable -- no session == no info"
