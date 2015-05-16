"""Display for Message screen."""
import pdb

from display import Display
from backend.session import SessionScope
from support.debug import debug


class MessageDisplay(Display):

    """Display for Message screen."""

    def __init__(self, core):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Messages"
        self._description = ""  # Who doesn't get a messages screen?
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
