"""NewGame message."""
from message import Message


class NewGame(Message):

    """Message to indicate creation of a new game."""

    def __init__(self, file_name=False):
        """Set file_name."""
        self.file_name = file_name

    def __str__(self):
        """Return string representation for object."""
        return "New Game"
