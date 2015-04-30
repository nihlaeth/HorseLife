"""Factory for Message model to simplify testing."""
import factory

from models.message import Message


class MessageFactory(factory.Factory):

    """Factory for Message model to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Message

    subject = "Hey"
    date = 0
    time = 0
    text = "Hello world!"
    read = False
