"""Provides an interface for the *Base classes."""
from eventbackend import EventBackend
from generators.eventgenerator import EventGenerator


class Backend(object):

    """Common methods for the *Base classes."""

    @classmethod
    def one(cls, session, id_):
        """Fetch instance from db with id and return backend instance."""
        pass

    @classmethod
    def all(cls, session):
        """Fetch all instances from db and return backend instances."""
        pass

    @classmethod
    def _one_id(cls, session, id_):
        """Fetch unencapsulated instance from database."""
        pass

    def __init__(self, id_):
        """Set the model identifier.

        _id indicates id of model in database.
        _str is used to indicate inherited class id in shared method.
        """
        self.id_ = id_
        self._str = "Backend"

    def get(self, session, t_stamp, key):
        """Get an attribute from the encapsulated db model.

        session -- sqlalchemy session
        t_stamp -- TimeStamp object indicating the current (game) time
        key -- name of the attribute to be fetched

        Note that fetching may have side effects in the model in question,
        some attributes are actively calculated and depend on the
        timestamp. If this is not the case (and you're sure), you can just
        pass None as timestamp.
        """
        instance = self._one_id(session, self.id_)
        info = instance.get(t_stamp, key)
        if info["e_info"] is not None:
            for event in info["e_info"]:
                self._update_event(session, event)
        return info["attr"]

    def set(self, session, key, value):
        """Set an attributes on the encapsulated db model.

        session -- sqlalchemy session
        key -- name of attribute
        value -- new value for attribute

        Note that this method does not require a timestamp. This is
        so because the 'active' attributes should never be set in this
        way. They have their own dedicated methods for this. You will
        get utter chaos if you try.
        """
        instance = self._one_id(session, self.id_)
        setattr(instance, key, value)

    def get_events(self, session, now):
        """Fetch events from encapsulated models and create them in db.

        session -- sqlalchemy session
        now -- TimeStamp object indicating 'current' time

        Note that this method should only be called once in the lifetime
        of the model. Not once in the instance lifetime, once per lifetime
        of the actual row in the database. Once these events are
        created, they will be updated, not removed and re-created.
        """
        instance = self._one_id(session, self.id_)

        events = {}
        result = instance.get_events(now)
        for e_info in result:
            if e_info is not None:
                events[e_info["subject"]] = {
                    "obj_id": self.id_,
                    "t_stamp": e_info["t_stamp"],
                    "callbacks": [[self._str, self.id_]]}
        EventGenerator.gen_many(session, events)

    def _update_event(self, session, e_info):
        """Update timestamp of an event associated with model.

        session -- sqlalchemy session
        e_info -- dict containing event information

        example e_info:
        {"subject": "some_event", "t_stamp": TimeStamp(0, 0), "msg": None}

        Note: "msg" has nothing to do with the event. It's simply a way
        for an event to emit a message to the user. It doesn't exactly
        deserve a beauty award, but I figured this was the best place
        for it.

        Note: this only updates the timestamp at which the event is
        next to be activated. If you wish to update callbacks, look
        somewhere else. If you do not increase the time associated
        with the event after calling it, the game will get stuck in
        an infinite loop.
        """
        event = EventBackend.one(session, e_info["subject"], self.id_)
        event.update(session, e_info["t_stamp"])
        if e_info["msg"] is not None:
            # TODO: get this ugly import out of here... for now
            # it's preventing a circular / dependency problem.
            from generators.messagegenerator import MessageGenerator
            MessageGenerator.gen_many(session, [e_info["msg"]])

    def event_callback(self, session, subject, t_stamp):
        """Execute event.

        This is called by the Time.pass_time method.

        session -- sqlalchemy session
        subject -- subject of the event (string)
        t_stamp -- TimeStamp object indicating the time at which
        the event fires. For all intense and purposes, this is
        the same as the current time, though it isn't in reality.
        """
        instance = self._one_id(session, self.id_)
        e_info = instance.event(subject, t_stamp)
        # self._update_event(session, e_info)
        return e_info
