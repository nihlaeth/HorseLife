from generator import Generator
from models.event import Event
from models.callback import Callback


class EventGenerator(Generator):
    @classmethod
    def _gen_one(cls, subject, date, time, callbacks):
        generated_callbacks = []
        for callback in callbacks:
            generated_callbacks.append(Callback(
                obj=callback[0],
                obj_id=callback[1]))
        return Event(
                date=date,
                time=time,
                subject=subject,
                callbacks=generated_callbacks)

    @classmethod
    def gen_many(cls, session, events):
        result = []
        for s in events:
            result.append(cls._gen_one(
                s,  # subject
                events[s][0],  # date
                events[s][1],  # time
                events[s][2]))  # callbacks
        session.add_all(result)
        return result
