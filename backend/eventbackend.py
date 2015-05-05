"""Provide abstraction layer for Event model."""
# Note: originally EventBackend inherited from Base. However,
# since I moved some common methods to Base to be inherited from,
# and some of them handle events, this resulted in circular imports.
# So for now, EventBackend doesn't inherit anything.
# from backend import Backend
from backend import Backend
from models.event import Event


class EventBackend(Backend):

    """Abstraction layer for Event model."""

    @classmethod
    def all(cls, session):
        """Return a list of all events encapsulated by EventBackend.

        session -- sqlalchemy session
        """
        models = session.query(Event).order_by(Event.date, Event.time)
        return [EventBackend(model.mid) for model in models]

    @classmethod
    def all_raw(cls, session):
        """Return a list of all events, ordered by date and time.

        These are unencapsulated events, so beware!

        session -- sqlalchemy session
        """
        return session.query(Event).order_by(Event.date, Event.time)

    # pylint: disable=arguments-differ
    @classmethod
    def one(cls, session, subject, obj_id):
        """Return a single encapsulated event.

        session -- sqlalchemy session
        subject -- event subject (string)
        obj_id -- id of the object this event belongs to (int)

        Not that obj_id does not say anything about the type of
        object this event belongs to. That's something that can
        be inferred from the subject, but is generally left for
        the callbacks to determine.
        """
        return EventBackend(
            session.query(Event).filter(
                Event.subject == subject,
                Event.obj_id == obj_id)[0].mid)

    @classmethod
    def next_event(cls, session):
        """Return the next (encapsulated) event (ordered chronologically).

        session -- sqlalchemy session

        Note: this method is used by pass_time to return the next event in
        queue. If the event in question is not updated (read: have it's
        timestamp set to some moment further into the future), it will
        keep activating the same event in an infinite loop. On the other
        side, if the event causes some other event to be moved forward
        in the queue, this will be handled correctly.

        Note: This method is currently unused as the event queue is now
        handled differently due to performance issues (too many queries).
        It's deprecated, and can disappear at any time!
        """
        return EventBackend(
            session.query(Event).order_by(Event.date, Event.time)[0].mid)

    @classmethod
    def _one_id(cls, session, id_):
        """Return the event that belongs to the id - for internal use only.

        session -- sqlalchemy session
        id -- model id (int)

        Note: this should never be called from anything other than this
        class. It returns the bare model instead of an encapsulated one.
        """
        return session.query(Event).filter_by(mid=id_)[0]

    def __init__(self, id_):
        """Set model id (does not connect to database).

        id -- model id (int)
        """
        Backend.__init__(self, id_)

    def update(self, session, timestamp):
        """Update timestamp on encapsulated model.

        session -- sqlalchemy session
        timestamp -- TimeStamp object with new time for event

        Note: Use this method to change event time, don't try to
        use set! Time is stored in a convenient TimeStamp which
        supports comparison and operators, and also in some
        simple integer fields, to avoid creating an extra
        table just for timestamps. Besides, I rather have
        timestamps operate without sessions, so they can
        be used anywhere in the layer model without breaking
        layer conventions (no session handling for example).
        """
        event = EventBackend._one_id(session, self.id_)
        event.update(timestamp)

    def string(self, session):
        """String representation for encapsulated event.

        session -- sqlalchemy session

        Note: since we want to print the info of the encapsulated
        model (we only keep an id handy, and that doesn't tell us
        nearly enough), we need a session. And since str() does
        not support extra arguments, and we can't store a session
        here without seriously smelling up the entire project, you're
        stuck using this ungainly method. Sorry.
        """
        event = EventBackend._one_id(session, self.id_)
        return str(event)
