from interface.cli.maindisplay import MainDisplay
from core import Core
from support.action import Action
from support.messages.quit import Quit


class MainCore(Core):
    def __init__(self):
        self._display = MainDisplay()

    def run(self):
        buildings = []
        # TODO: fetch buildings from backend
        actions = []
        for b in buildings:
            actions.append(Action(BuildingCore(), [b]))
        
        menu = []
        menu.append(Action(Quit()))

        self._display.init(actions, menu)
        choice = self._display.display()

        # TODO: decide what to do with the input

        return choice

    def __str__(self):
        return "Main"
