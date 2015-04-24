"""SavedGame message."""
from message import Message


class SavedGame(Message):

    """Message indicating a saved game should be loaded."""

    def __init__(self, file_name):
        """Set file_name."""
        self.file_name = file_name

    def __str__(self):
        """Return string representation of object."""
        return self.file_name
