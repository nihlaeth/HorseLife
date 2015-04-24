"""Interface to inherit from for message classes."""


class Message(object):

    """Messenger class -- to be inherited from."""

    def __str__(self):
        """Return string representation for object."""
        return "Message"
