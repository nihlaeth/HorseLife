from backend import Backend
from models.person import Person


class PersonBackend(Backend):
    @classmethod
    def all(cls, session):
        """ Return a list of all people (encapsulated)"""
        models = session.query(Person)
        return [PersonBackend(person.id) for person in models]

    @classmethod
    def one(cls, session, name):
        """ Return encapsulated person, selected by (unique) name."""
        return PersonBackend(session.query(Person).filter_by(name=name)[0].id)

    @classmethod
    def _one_id(cls, session, id):
        """ Return bare person - internal use only!"""
        return session.query(Person).filter_by(id=id)[0]

    def __init__(self, id):
        """ Set model id"""
        self._id = id
