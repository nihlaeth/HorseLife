"""Display for Main screen."""
import pdb

from errors.invalidchoice import InvalidChoice
from display import Display
from pasturedisplay import PastureDisplay
from stabledisplay import StableDisplay
from towndisplay import TownDisplay
from messagedisplay import MessageDisplay
from core.core import Core
from core.stablecore import StableCore
from core.pasturecore import PastureCore
from core.towncore import TownCore
from core.messagecore import MessageCore
from backend.session import SessionScope
from support.debug import debug
from support.messages.quit import Quit
from support.messages.back import Back


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
            self._info = self._core.get_info(session)
            self._menu = self._core.get_menu(session)
            self._actions = self._core.get_actions(session)
            self._story = self._core.get_story(session)
            self._level = self._core.get_level(session)

            choice = Display.display(self, self._level)

            result = self._core.choice(session, choice)

            if debug():
                pdb.set_trace()

            if result is None:
                return self.display()
            elif isinstance(result, Core):
                if isinstance(result, StableCore):
                    next_display = StableDisplay()
                elif isinstance(result, TownCore):
                    next_display = TownDisplay()
                elif isinstance(result, PastureCore):
                    next_display = PastureDisplay()
                elif isinstance(result, MessageCore):
                    next_display = MessageDisplay()
                next_action = next_display.display()
                if isinstance(next_action, Back):
                    return self.display()
                elif isinstance(next_action, Quit):
                    return next_action
                else:
                    raise InvalidChoice(result)
            elif isinstance(result, Back) or isinstance(result, Quit):
                return result
            else:
                raise InvalidChoice(result)
