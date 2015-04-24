"""Back message."""
from message import Message


# No need for an init, attribute-less object
# pylint: disable=no-init
class Back(Message):

    """Message to indicate moving a level up in the call stack."""

    def __str__(self):
        """Kinda speaks for itself."""
        return "Back"
