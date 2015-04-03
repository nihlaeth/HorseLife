from interface.cli.maindisplay import MainDisplay
from core import Core
from buildingcore import BuildingCore
from support.messages.quit import Quit
from backend.session import session_scope
from backend.stablesbackend import StablesBackend


class MainCore(Core):
    def __init__(self):
        self._display = MainDisplay()

    def run(self):
        while True:
            with session_scope() as session:
                stables = StablesBackend.all(session)

                from backend.time import time
                info = [" ".join(["Time", time.get_time()])]

                actions = []
                for s in stables:
                    actions.append(BuildingCore(s))

                menu = []
                menu.append(Quit())

                self._display.init(actions, menu, info)
                choice = self._display.display()
                if isinstance(choice, Quit):
                    return choice
                elif isinstance(choice, BuildingCore):
                    result = choice.run()

                if result is not None:
                    if isinstance(result, Quit):
                        return result
                    # if it's of type Back, just display
                    # this screen again - continue loop.
                session.commit()

    def __str__(self):
        return "Main"
