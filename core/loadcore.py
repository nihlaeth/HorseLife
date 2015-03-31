from os import listdir
import os.path

from core import Core
from interface.cli.loaddisplay import LoadDisplay
from support.action import Action
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from support.messages.quit import Quit

class LoadCore(Core):
    def __init__(self):
        self._display = LoadDisplay()

    def run(self):
        files = os.listdir("./saves/")
        actions = []
        for f in files:
            action.append(Action(SavedGame(f),[]))
        menu = []
        menu.append(Action(NewGame()))
        menu.append(Action(Quit()))

        self._display.init(actions, menu)
        choice = self._display.display()
        if isinstance(choice.cls, NewGame):
            name = self._display.get_string(4, "Name your game: ")
            choice.cls.file_name = name
        return choice

    def __str__(self):
        return "Load Game"
