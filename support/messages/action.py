"""Action message."""
from message import Message


class Action(Message):

    """Action message.

    Container for actions, for example clean a stable, groom a horse.
    """

    def __init__(self, action, description, arguments=None, level=0):
        """Set action, description and optional arguments."""
        self.action = action
        self.description = description
        if arguments is None:
            arguments = []
        self.arguments = arguments
        self.min_level = level

    def __str__(self):
        """Return string representation of object."""
        return self.description
