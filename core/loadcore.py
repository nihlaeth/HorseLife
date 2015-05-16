"""Game logic for loading a saved or new game."""
import os

from core import Core
from errors.invalidchoice import InvalidChoice
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame


class LoadCore(Core):

    """This lets the user pick a saved game, or start (and name) a new one."""

    def __init__(self):
        """Set display."""
        Core.__init__(self)

    def get_info(self, _):
        """Return an empty list.

        There is no database at this point, do not call parent get_info
        method.
        """
        return []

    def get_level(self, _):
        """Return 0.

        Again, no database at this point, do not call parent get_level
        method.
        """
        return 0

    def get_story(self, _):
        """Return None.

        No database at this point.
        """
        return None

    def get_actions(self, _):
        """Return action list."""
        files = os.listdir("./saves/")
        actions = []
        for file_ in files:
            actions.append(SavedGame(file_))
        return actions

    def get_menu(self):
        """Return menu list."""
        menu = [NewGame()] + Core.get_menu(self)
        return menu

    # pylint: disable=arguments-differ
    def choice(self, _, choice):
        """Handle user choice."""
        result = Core.choice(self, None, choice)
        if result == "handled":
            return None
        elif result is None:
            if isinstance(choice, NewGame) or isinstance(choice, SavedGame):
                return choice
            else:
                raise InvalidChoice(choice)
        else:
            return result

    def __str__(self):
        """Return string interpretation of object."""
        return "Load Game"
