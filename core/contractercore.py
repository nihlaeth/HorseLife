from interface.cli.contracterdisplay import ContracterDisplay
from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.command import Command
from support.messages.action import Action
from backend.session import session_scope


class ContracterCore(Core):
    def __init__(self):
        self._display = ContracterDisplay()

    def run(self):
        while True:
            with session_scope() as session:
                from backend.time import time
                info = [" ".join(["Time", time.get_time()])]
                info.append("What do you want constructed?")

                actions = [
                        Action("stables", "Stables"),
                        Action("pastures", "Pastures"),
                        Action("arenas", "Arenas"),
                        Action("tack-feed", "Tack and feed rooms")]

                menu = [Back(), Quit()]

                self._display.init(actions, menu, info)
                choice = self._display.display()
                if isinstance(choice, Quit) or isinstance(choice, Back):
                    return choice
                elif isinstance(choice, Command):
                    exec(choice.command)

                session.commit()

    def __str__(self):
        return "Town"
