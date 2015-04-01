from interface.cli.maindisplay import MainDisplay
from core import Core
from buildingcore import BuildingCore
from support.messages.quit import Quit
from backend.buildingsbackend import BuildingsBackend


class MainCore(Core):
    def __init__(self):
        self._display = MainDisplay()

    def run(self):
        while True:
            buildings = BuildingsBackend.all()
            actions = []
            for b in buildings:
                actions.append(BuildingCore(b))

            menu = []
            menu.append(Quit())

            self._display.init(actions, menu)
            choice = self._display.display()
            if isinstance(choice, Quit):
                return choice
            # If it's anything else, just display
            # the main screen again.

    def __str__(self):
        return "Main"
