"""Display for Load screen."""
import pdb

from support.debug import debug
from display import Display
from support.messages.newgame import NewGame
from support.messages.savedgame import SavedGame
from errors.invalidchoice import InvalidChoice


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

        try:
            return self.choice(result)
        except InvalidChoice:
            if isinstance(result, NewGame):
                result.file_name = self.get_string(4, "Name your game: ")
                return result
            elif isinstance(result, SavedGame):
                return result
            else:
                raise InvalidChoice(result)
