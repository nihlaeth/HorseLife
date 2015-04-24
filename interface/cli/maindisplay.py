"""Display for Main screen."""
from display import Display


class MainDisplay(Display):

    """Display for Main screen."""

    def __init__(self):
        """Set title and description."""
        Display.__init__(self)
        self._title = "HorseLife"
        self._description = (
            "Welcome to HorseLife!\n\n"
            "Below is a list of buildings on your property. To enter one,"
            "type their associated number and hit enter!")
