"""Command message."""
from message import Message


class Command(Message):

    """Signal the interface module to display a meter."""

    def __init__(self, command):
        """Set command."""
        self.command = command

    def __str__(self):
        """Return string representation of object."""
        return ' '.join(["Command:", self.command])
