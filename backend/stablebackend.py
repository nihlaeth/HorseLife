from backend import Backend
from eventbackend import EventBackend
from models.stable import Stable
from generators.eventgenerator import EventGenerator


class StableBackend(Backend):
    @classmethod
    def all(cls, session):
        """ Return a list of all encapsulated stable models.

        session -- sqlalchemy session
        """
        stables = session.query(Stable).order_by(Stable.name)
        return [StableBackend(stable.id) for stable in stables]

    @classmethod
    def _one_id(cls, session, id):
        """ Return bare stable model - internal use only!

        session -- sqlalchemy session
        id -- model id (int)
        """
        return session.query(Stable).filter_by(id=id)[0]

    def __init__(self, id):
        """ Backend sets _id, _str is for use with inherited methods."""
        Backend.__init__(self, id)
        self._str = "StableBackend"

    def clean(self, session, now):
        """ Execute clean method on encapsulated model.

        session -- sqlalchemy session
        now -- TimeStamp object indicating time at the start of this action
        return: TimeStamp object indicating the time at the end of action
        """
        stable = self._one_id(session, self._id)
        result = stable.clean(now)
        self._update_event(session, result["e_info"])
        return result["clock"]

    def food(self, session):
        """ Add food to encapsulated stable.

        session -- sqlalchemy session

        Note: this does not take care of side effects like food supply,
        all it does is fill the feeding tray in this particular stable.
        In the future, we'll want to do something with types of food.
        """
        stable = self._one_id(session, self._id)
        return stable.food()

    def water(self, session):
        """ Provide water for encapsulated stable.

        session -- sqlalchemy
        """
        stable = self._one_id(session, self._id)
        return stable.water()

    def __repr__(self):
        # TODO find elegant way to get repr info
        # without a session - and have the info not
        # be stale.
        return "Stable -- no session == no info"

    def __str__(self):
        # TODO same as above
        return "Stable -- no session == no info"
