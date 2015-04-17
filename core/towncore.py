from interface.cli.towndisplay import TownDisplay
from core import Core
from contractercore import ContracterCore
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.command import Command
from support.messages.action import Action
from backend.session import session_scope


class TownCore(Core):
    def __init__(self):
        self._display = TownDisplay()

    def run(self):
        while True:
            with session_scope() as session:
                from backend.time import time
                info = [" ".join(["Time", time.get_time(session)])]
                info.append("Where do you want to visit?")

                actions = [
                        Action("bank", "Bank"),
                        Action("horses", "Horse market"),
                        Action("contracter", "Contracter"),
                        Action("tack", "Saddle maker"),
                        Action("food", "Horse supplies"),
                        Action("newspaper", "News agency"),
                        Action("veterinarian", "Veterinarian"),
                        Action("farrier", "Farrier"),
                        Action("competitions",
                               "National equine sports association"),
                        Action("employment", "Employment agency"),
                        Action("education", "College")]
                menu = [Back(), Quit()]

                self._display.init(actions, menu, info)
                choice = self._display.display()
                if isinstance(choice, Quit) or isinstance(choice, Back):
                    return choice
                elif isinstance(choice, Command):
                    exec(choice.command)
                    result = None
                elif isinstance(choice, Action):
                    if choice.action == "contracter":
                        result = ContracterCore().run()

                if isinstance(result, Quit):
                    return result
                session.commit()

    def __str__(self):
        return "Town"
