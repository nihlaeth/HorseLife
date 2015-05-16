"""Display for Contracter store."""
import pdb

from display import Display
from backend.session import SessionScope
from support.debug import debug


class ContracterDisplay(Display):

    """Display for Contracter store."""

    def __init__(self, core):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Contracter"
        self._description = ""
        # self._description = (
        #     "Welcome!\n"
        #     "If you need some construction done, "
        #     "You've come to the right place! We're "
        #     "extremely fast, and land costs are included "
        #     "in all our prices. Happy shopping!")
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
