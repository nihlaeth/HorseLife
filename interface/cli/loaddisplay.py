"""Display for Load screen."""
import pdb

from support.debug import debug
from display import Display
from support.messages.newgame import NewGame


class LoadDisplay(Display):

    """Display for Load screen."""

    def __init__(self, core):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Select game"
        self._description = (
            "Welcome to HorseLife!\n\n"
            "Select an existing game below, or create a new game.")
        self._core = core

    # pylint: disable=arguments-differ
    def display(self):
        """Do some displaying."""
        self.init(None)

        result = self._core.choice(None, self._choice)

        if debug():
            pdb.set_trace()

        if result is None:
            return self.display()
        elif isinstance(result, NewGame):
            result.file_name = self.get_string(4, "Name your game: ")
            return result
        else:
            # Hanlde SavedGame, Back and Quit the same way.
            return result
