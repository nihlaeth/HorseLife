from eventbackend import EventBackend
from generators.eventgenerator import EventGenerator


class Backend():
    @classmethod
    def one(cls, id):
        """ Fetch instance from db with id and return backend instance."""
        pass

    @classmethod
    def all(cls):
        """ Fetch all instances from db and return list of backend
        instances.
        """
        pass

    def __init__(self, id):
        """ _id indicates id of model in database, _str is used in
        classes that inherit from this one, to differentiate between
        them in common methods.
        """
        self._id = id
        self._str = "Backend"

    def get(self, session, t_stamp, key):
        """ Get an attribute from the encapsulated db model.

        session -- sqlalchemy session
        t_stamp -- TimeStamp object indicating the current (game) time
        key -- name of the attribute to be fetched

        Note that fetching may have side effects in the model in question,
        some attributes are actively calculated and depend on the
        timestamp. If this is not the case (and you're sure), you can just
        pass None as timestamp.
        """
        instance = self._one_id(session, self._id)
        info = instance.get(t_stamp, key)
        if info["e_info"] is not None:
            self._update_event(session, info["e_info"])
        return info["attr"]

    def set(self, session, key, value):
        """ Set an attributes on the encapsulated db model.

        session -- sqlalchemy session
        key -- name of attribute
        value -- new value for attribute

        Note that this method does not require a timestamp. This is
        so because the 'active' attributes should never be set in this
        way. They have their own dedicated methods for this. You will
        get utter chaos if you try.
        """
        instance = self._one_id(session, self._id)
        setattr(instance, key, value)

    def get_events(self, session, now):
        """ Fetches event information from encapsulated model and creates
        the necessary events.

        session -- sqlalchemy session
        now -- TimeStamp object indicating 'current' time

        Note that this method should only be called once in the lifetime
        of the model. Not once in the instance lifetime, once per lifetime
        of the actual row in the database. Once these events are
        created, they will be updated, not removed and re-created.
        """
        instance = self._one_id(session, self._id)

        events = {}
        result = instance.get_events(now)
        for e_info in result:
            if e_info is not None:
                events[e_info["subject"]] = {
                        "obj_id": self._id,
                        "date": e_info["t_stamp"].date,
                        "time": e_info["t_stamp"].time,
                        "callbacks": [[self._str, self._id]]}
        EventGenerator.gen_many(session, events)

    def _update_event(self, session, e_info):
        """ Update timestamp of an event associated with the encapsulated
        model.

        session -- sqlalchemy session
        e_info -- dict containing event information

        example e_info:
        {"subject": "some_event", "t_stamp": TimeStamp(0, 0)}

        Note: this only updates the timestamp at which the event is
        next to be activated. If you wish to update callbacks, look
        somewhere else. If you do not increase the time associated
        with the event after calling it, the game will get stuck in
        an infinite loop.
        """
        event = EventBackend.one(session, e_info["subject"], self._id)
        event.update(session, e_info["t_stamp"])

    def event_callback(self, session, subject, t_stamp):
        """ This method is called at event activation.

        session -- sqlalchemy session
        subject -- subject of the event (string)
        t_stamp -- TimeStamp object indicating the time at which
        the event fires. For all intense and purposes, this is
        the same as the current time, though it isn't in reality.
        """
        instance = self._one_id(session, self._id)
        e_info = instance.event(subject, t_stamp)
        self._update_event(session, e_info)
