from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.meter import Meter
from support.messages.action import Action
from support.messages.command import Command
from interface.cli.stabledisplay import StableDisplay
from backend.session import session_scope
from backend.stablesbackend import StablesBackend
from backend.horsesbackend import HorsesBackend


class StableCore(Core):
    def __init__(self, stable):
        self._stable_id = stable.id
        self._stable = stable
        self._display = StableDisplay()
        if len(self._stable.horses) == 1:
            self._horse = self._stable.horses[0]
            self._horse_id = self._horse.id
        else:
            self._horse = None

    def run(self):
        while True:
            with session_scope() as session:
                # Make sure the stable and horse instances are fresh.
                self._stable = StablesBackend.one(session, self._stable_id)
                if self._horse is not None:
                    self._horse = HorsesBackend.one(session, self._horse_id)

                from backend.time import time
                info = [" ".join(["Time:", time.get_time()]),
                        "",
                        "Cleanliness:",
                        Meter(self._stable.cleanliness)]

                if self._horse is not None:
                    info.append("")
                    info.append(''.join(["Name: ", self._horse.name]))
                    info.append("Happiness:")
                    info.append(Meter(self._horse.happiness))
                    info.append("Health:")
                    info.append(Meter(self._horse.health))
                    info.append("Food:")
                    info.append(Meter(self._horse.food))
                    info.append("Water:")
                    info.append(Meter(self._horse.water))
                    info.append("Energy:")
                    info.append(Meter(self._horse.energy))
                    info.append("Exercise:")
                    info.append(Meter(self._horse.energy))
                    info.append("Hygiene:")
                    info.append(Meter(self._horse.hygiene))
                    info.append("Stimulation:")
                    info.append(Meter(self._horse.stimulation))
                    info.append("Environment:")
                    info.append(Meter(self._horse.environment))
                    info.append("Social:")
                    info.append(Meter(self._horse.social))

                actions = []
                actions.append(Action("clean", "Clean stable"))
                actions.append(Action("feed", "Fill food tray"))
                actions.append(Action("water", "Fill waterbucket"))
                if self._horse is not None:
                    actions.append(Action("groom", "Groom horse"))
                    actions.append(Action("pet", "Pet horse"))
                    actions.append(Action("treat", "Feed treat"))
                    actions.append(Action("training journal",
                                          "View training journal"))
                    actions.append(Action("pedigree",
                                          "View pedigree papers"))
                    actions.append(Action("change name", "Change name"))

                if len(self._stable.horses) > 1:
                    for horse in self._stable.horses:
                        if horse != self._horse:
                            actions.append(Action(
                                "fetch",
                                ''.join(["Fetch ", horse.name]),
                                [horse]))

                menu = [Back(), Quit()]
                self._display.init(actions, menu, info)
                choice = self._display.display()
                if isinstance(choice, Quit) or isinstance(choice, Back):
                    return choice
                elif isinstance(choice, Command):
                    exec(choice.command)
                elif isinstance(choice, Action):
                        if choice.action == "clean":
                            self._stable.clean()
                        if choice.action == "change name":
                            self._horse.name = self._display.get_string(
                                    4,
                                    "Name: ")
                        if choice.action == "groom":
                            self._horse.groom()
                        if choice.action == "feed":
                            self._stable.food()
                            # TODO fetch food from storage
                        if choice.action == "water":
                            self._stable.water()
                        if choice.action == "pet":
                            self._horse.pet()
                session.commit()

    def __str__(self):
        return self._stable.name
