"""Interface to inherit from for *Core classes."""


class Core(object):

    """Common methods to inherit for *Core classes."""

    def __init__(self):
        """Get a display."""
        self._display = None

    def run(self):
        """Game logic.

        Get data through backend and frontend (interface
        / user input), and do stuff with it! Communicate back to backend
        and front-end, well, you get the picture.
        """
        pass

    def __str__(self):
        """Return string interpretation of object."""
        return "Core"
