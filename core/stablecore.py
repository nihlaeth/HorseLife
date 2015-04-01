from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from interface.cli.stabledisplay import StableDisplay

class StableCore(Core):
    def __init__(self, stable):
        self._stable = stable
        self._display = StableDisplay()

    def run(self):
        while True:
            info = []
            actions = []
            menu = [Quit(), Back()]
            self._display.init(actions, menu, info)
            choice = self._display.display()
            if isinstance(choice, Quit) or isinstance(choice, Back):
                return choice

    def __str__(self):
        return self._stable.name
