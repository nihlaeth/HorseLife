"""Display for Main screen."""
import pdb

from display import Display
from backend.session import SessionScope
from support.debug import debug


# pylint: disable=too-many-instance-attributes
class MainDisplay(Display):

    """Display for Main screen."""

    def __init__(self, core):
        """Set title and description."""
        Display.__init__(self)
        self._title = "HorseLife"
        self._description = ""
        # self._description = (
        #     "Welcome to HorseLife!\n\n"
        #     "Below is a list of buildings on your property. To enter one,"
        #     "type their associated number and hit enter!")
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
