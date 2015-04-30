"""Display for Message screen."""
from display import Display


class MessageDisplay(Display):

    """Display for Message screen."""

    def __init__(self):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Messages"
        self._description = ""  # Who doesn't get a messages screen?
