"""Display for Load screen."""
from display import Display


class LoadDisplay(Display):

    """Display for Load screen."""

    def __init__(self):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Select game"
        self._description = (
            "Welcome to HorseLife!\n\n"
            "Select an existing game below, or create a new game.")
