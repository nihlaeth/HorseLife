"""Provide abstraction layer for Person model."""
from backend import Backend
from models.person import Person


class PersonBackend(Backend):

    """Abstraction layer for Person model."""

    @classmethod
    def all(cls, session):
        """Return a list of all people (encapsulated)."""
        models = session.query(Person)
        return [PersonBackend(session, person.mid) for person in models]

    @classmethod
    def one(cls, session, name):
        """Return encapsulated person, selected by (unique) name."""
        return PersonBackend(
            session,
            session.query(Person).filter_by(name=name)[0].mid)

    @classmethod
    def active_player(cls, session):
        """Return the active player.

        For now, we just return the player with id=1. In the future, with
        multiple active players, this will be a bit more complicated.
        """
        return PersonBackend(session, 1)

    @classmethod
    def _one_id(cls, session, id_):
        """Return bare person - internal use only."""
        return session.query(Person).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Set model id."""
        Backend.__init__(self, session, id_)
        self._cls = "PersonBackend"

    def spend_money(self, session, transaction):
        """Spend money.

        This figures out if there's enough of it, and if so, subtracts
        the right amount and creates a transaction.
        """
        person = self._one_id(session, self.id_)
        return person.spend_money(transaction)
