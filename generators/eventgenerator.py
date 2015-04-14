from generator import Generator
from models.event import Event
from models.callback import Callback


class EventGenerator(Generator):
    @classmethod
    def _gen_one(cls, subject, obj_id, date, time, callbacks):
        """ Generate a single event object."""
        generated_callbacks = []
        for callback in callbacks:
            generated_callbacks.append(Callback(
                obj=callback[0],
                obj_id=callback[1]))
        return Event(
                date=date,
                time=time,
                subject=subject,
                obj_id=obj_id,
                callbacks=generated_callbacks)

    @classmethod
    def gen_many(cls, session, events):
        """ Generate 1 or more events and add them to the session."""
        result = []
        for s in events:
            result.append(cls._gen_one(
                s,  # subject
                events[s]["obj_id"],
                events[s]["date"],
                events[s]["time"],
                events[s]["callbacks"]))
        session.add_all(result)
        return result
