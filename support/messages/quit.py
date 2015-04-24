"""Quit message."""
from message import Message


class Quit(Message):

    """Message to indicate shutdown."""

    def __str__(self):
        """Return string representation for object."""
        return "Quit"
