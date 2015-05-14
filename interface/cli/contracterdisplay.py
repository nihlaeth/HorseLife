"""Display for Contracter store."""
import pdb

from display import Display
from messagedisplay import MessageDisplay
from backend.session import SessionScope
from core.messagecore import MessageCore
from support.debug import debug
from support.messages.back import Back
from support.messages.quit import Quit


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

            if result is None:
                return self.display()
            elif isinstance(result, MessageCore):
                next_action = MessageDisplay().display()
                if isinstance(next_action, Back):
                    return self.display()
                elif isinstance(next_action, Quit):
                    return next_action
            elif isinstance(result, Back) or isinstance(result, Quit):
                return result
