"""Generator for Messages model."""
from generator import Generator
from models.message import Message


class MessageGenerator(Generator):

    """Generator for Message model."""

    # pylint: disable=arguments-differ
    @classmethod
    def _gen_one(cls, subject, t_stamp, text):
        """Generate single Message model."""
        return Message(
            subject=subject,
            time=t_stamp.time,
            date=t_stamp.date,
            text=text,
            read=False)

    @classmethod
    def gen_many(cls, session, messages):
        """Generate one or more messages."""
        result = []
        for message in messages:
            result.append(cls._gen_one(
                message["subject"],
                message["t_stamp"],
                message["text"]))
        session.add_all(result)
        session.flush()
        return result
