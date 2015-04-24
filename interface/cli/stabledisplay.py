"""Display for Stable screen."""
from display import Display


class StableDisplay(Display):

    """Display for Stable screen."""

    def __init__(self):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Stable"
        self._description = (
            "Welcome to the stable!\n\n"
            "Here you can groom your horse, "
            "take it for a ride, and check "
            "how it's doing.")
