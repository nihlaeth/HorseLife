from interface.cli.maindisplay import MainDisplay
from core import Core
from buildingcore import BuildingCore
from towncore import TownCore
from support.messages.quit import Quit
from support.messages.command import Command
from backend.session import session_scope
from backend.stablebackend import StableBackend


class MainCore(Core):
    def __init__(self):
        self._display = MainDisplay()

    def run(self):
        while True:
            with session_scope() as session:
                stables = StableBackend.all(session)

                from backend.time import time
                info = [" ".join(["Time", time.get_time(session)])]

                actions = [TownCore()]
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
                elif isinstance(choice, TownCore):
                    result = choice.run()
                elif isinstance(choice, Command):
                    exec(choice.command)
                    result = None

                if result is not None:
                    if isinstance(result, Quit):
                        return result
                    # if it's of type Back, just display
                    # this screen again - continue loop.
                session.commit()

    def __str__(self):
        return "Main"
