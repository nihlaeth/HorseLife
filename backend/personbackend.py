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
    def _one_id(cls, session, id_):
        """Return bare person - internal use only."""
        return session.query(Person).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Set model id."""
        Backend.__init__(self, session, id_)
        self._cls = "PersonBackend"
