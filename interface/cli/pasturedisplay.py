"""Display for Pasture screen."""
import pdb

from display import Display
from support.debug import debug
from backend.session import SessionScope


class PastureDisplay(Display):

    """Display for Pasture screen."""

    def __init__(self, core):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Pasture / paddock"
        self._description = ""
        self._core = core

    # pylint: disable=arguments-differ
    def display(self):
        """Do some displaying."""
        with SessionScope() as session:
            self.init(session)

            result = self._core.choice(session, self._choice)

            if debug():
                pdb.set_trace()

            return self.choice(result)
