"""Display for Town screen."""
from display import Display


class TownDisplay(Display):

    """Display for Town screen."""

    def __init__(self):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Town"
        self._description = ("Welcome to the town center!")
