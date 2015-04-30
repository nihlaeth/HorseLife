"""Provide abstraction layer for Message model."""
from backend import Backend
from models.message import Message


class MessageBackend(Backend):

    """Abstraction layer for Message model."""

    @classmethod
    def all(cls, session):
        """Return a list of all messages (encapsulated)."""
        models = session.query(Message).order_by(Message.date, Message.time)
        return [MessageBackend(model.mid) for model in models]

    @classmethod
    def one(cls, session, mid):
        """Return encapsulated message."""
        return MessageBackend(session.query(Message).filter_by(mid=mid)[0].mid)

    @classmethod
    def unread(cls, session):
        """Return number of unread messages."""
        return session.query(Message).filter_by(read=False).count()

    @classmethod
    def _one_id(cls, session, mid):
        """Return raw model."""
        return session.query(Message).filter_by(mid=mid)[0]

    def __init__(self, mid):
        """Set model id."""
        Backend.__init__(self, mid)
        self._str = "MessageBackend"

    def set(self, session, key, value):
        """Set attribute on encapsulated model."""
        message = MessageBackend._one_id(session, self.id_)
        message.set(key, value)
