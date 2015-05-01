"""Game logic for loading a saved or new game."""
import os
import pdb

from core import Core
from interface.cli.loaddisplay import LoadDisplay
from support.debug import debug
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from support.messages.quit import Quit


class LoadCore(Core):

    """This lets the user pick a saved game, or start (and name) a new one."""

    def __init__(self):
        """Set display."""
        Core.__init__(self)
        self._display = LoadDisplay()

    def run(self):
        """Run with it."""
        while True:
            files = os.listdir("./saves/")
            actions = []
            for file_ in files:
                actions.append(SavedGame(file_))
            menu = []
            menu.append(NewGame())
            menu.append(Quit())

            self._display.init(actions, menu)
            choice = self._display.display()
            if debug():
                pdb.set_trace()
            if isinstance(choice, NewGame):
                name = self._display.get_string(4, "Name your game: ")
                choice.file_name = name
                return choice
            elif isinstance(choice, SavedGame):
                return choice
            elif isinstance(choice, Quit):
                return choice

    def __str__(self):
        """Return string interpretation of object."""
        return "Load Game"
