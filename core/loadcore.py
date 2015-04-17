from os import listdir
import os.path

from core import Core
from interface.cli.loaddisplay import LoadDisplay
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from support.messages.quit import Quit
from support.messages.command import Command


class LoadCore(Core):
    def __init__(self):
        self._display = LoadDisplay()

    def run(self):
        while True:
            files = os.listdir("./saves/")
            actions = []
            for f in files:
                action.append(SavedGame(f))
            menu = []
            menu.append(NewGame())
            menu.append(Quit())

            self._display.init(actions, menu)
            choice = self._display.display()
            if isinstance(choice, NewGame):
                name = self._display.get_string(4, "Name your game: ")
                choice.file_name = name
                return choice
            elif isinstance(choice, SavedGame):
                return choice
            elif isinstance(choice, Command):
                exec(choice.command)
            elif isinstance(choice, Quit):
                return choice

    def __str__(self):
        return "Load Game"
