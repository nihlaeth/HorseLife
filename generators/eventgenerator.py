"""Generator for Event model."""
from generator import Generator
from models.event import Event
from models.callback import Callback


# This class does not need an init, it only has classmethods.
# pylint: disable=no-init
class EventGenerator(Generator):

    """Generator for Event model."""

    # The arguments are supposed to be different.
    # pylint: disable=arguments-differ
    @classmethod
    def _gen_one(cls, subject, obj_id, t_stamp, callbacks):
        """Generate a single event object.

        subject -- subject of the event
        obj_id -- id of the db row / model id
        t_stamp -- TimeStamp at which the event is to be activated
        callbacks -- list of CallBack objects to be called at activation
        """
        generated_callbacks = []
        for callback in callbacks:
            generated_callbacks.append(Callback(
                obj=callback[0],
                obj_id=callback[1]))
        return Event(
            date=t_stamp.date,
            time=t_stamp.time,
            subject=subject,
            obj_id=obj_id,
            callbacks=generated_callbacks)

    @classmethod
    def gen_many(cls, session, events):
        """Generate 1 or more events and add them to the session."""
        result = []
        for subject in events:
            result.append(cls._gen_one(
                subject,
                events[subject]["obj_id"],
                events[subject]["t_stamp"],
                events[subject]["callbacks"]))
        session.add_all(result)
        session.flush()
        return result
