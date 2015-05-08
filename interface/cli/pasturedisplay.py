"""Display for Pasture screen."""
from display import Display


class PastureDisplay(Display):

    """Display for Pasture screen."""

    def __init__(self):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Pasture / paddock"
        self._description = ""
