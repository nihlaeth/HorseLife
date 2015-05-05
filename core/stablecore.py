"""Game logic for Stable screen."""
import pdb

from core import Core
from messagecore import MessageCore
from support.debug import debug
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.meter import Meter
from support.messages.action import Action
from interface.cli.stabledisplay import StableDisplay
from backend.session import SessionScope
from backend.horsebackend import HorseBackend
from backend.time import Time


class StableCore(Core):

    """Game logic for Stable screen.

    View a stable (and it's inhabitants). This is the main starting
    point for doing anything with a horse.
    """

    def __init__(self, stable):
        """Get display and set stable and horse private attributes.

        stable -- StableBackend instance
        """
        Core.__init__(self)
        self._stable = stable
        self._display = StableDisplay()
        self._horse = None

    def _horse_info(self, session, info, now):
        """Provide information on the horse."""
        info.append("")
        info.append(''.join([
            "Name: ",
            self._horse.get(session, None, "name")]))
        info.append("Happiness:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "happiness")))
        info.append("Health:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "health")))
        info.append("Food:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "food")))
        info.append("Water:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "water")))
        info.append("Energy:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "energy")))
        info.append("Exercise:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "energy")))
        info.append("Hygiene:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "hygiene")))
        info.append("Stimulation:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "stimulation")))
        info.append("Environment:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "environment")))
        info.append("Social:")
        info.append(Meter(self._horse.get(
            session,
            now,
            "social")))

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                # Get horses
                horses = self._stable.get(session, None, "horses")
                if len(horses) > 0 and self._horse is None:
                    self._horse = HorseBackend(horses[0].mid)

                time = Time(session)
                now = time.get_time_stamp(session)
                info = self._info(session)
                info.append("")
                info.append("Cleanliness:")
                info.append(Meter(self._stable.get(
                    session,
                    now,
                    "cleanliness")))

                if self._horse is not None:
                    # Lists are passed by reference by default
                    self._horse_info(session, info, now)
                actions = []
                actions.append(Action("clean", "Clean stable"))
                actions.append(Action("feed", "Fill food tray"))
                actions.append(Action("water", "Fill waterbucket"))
                if self._horse is not None:
                    actions.append(Action("groom", "Groom horse"))
                    actions.append(Action("pet", "Pet horse"))
                    actions.append(Action("treat", "Feed treat"))
                    actions.append(Action("training journal",
                                          "View training journal",
                                          level=1))
                    actions.append(Action("pedigree",
                                          "View pedigree papers",
                                          level=5))
                    actions.append(Action("change name", "Change name"))

                if len(horses) > 1:
                    for horse in horses:
                        if horse.id != self._horse.id_:
                            actions.append(Action(
                                "fetch",
                                ''.join(["Fetch ", horse.name]),
                                [HorseBackend(horse.id)]))

                menu = [Back(), Quit()]
                story = self.get_story(session)
                self._display.init(actions, menu, info, story)
                choice = self._display.display()
                if debug():
                    pdb.set_trace()
                result = self._choice(session, choice, time, now)
                if isinstance(result, Quit) or isinstance(result, Back):
                    return result

    def _choice(self, session, choice, time, now):
        """Handle user choice."""
        if isinstance(choice, Quit) or isinstance(choice, Back):
            return choice
        elif isinstance(choice, Action):
            if choice.action == "clean":
                new_time = self._stable.clean(session, now)
                time.pass_time(session, new_time)
            elif choice.action == "change name":
                self._horse.set(session, "name", self._display.get_string(
                    4,
                    "Name: "))
            elif choice.action == "groom":
                new_time = self._horse.groom(session, now)
                time.pass_time(session, new_time)
            elif choice.action == "feed":
                new_time = self._stable.food(session, now)
                time.pass_time(session, new_time)
                # TODO fetch food from storage
            elif choice.action == "water":
                new_time = self._stable.water(session, now)
                time.pass_time(session, new_time)
            elif choice.action == "pet":
                new_time = self._horse.pet(session, now)
                time.pass_time(session, new_time)
            elif choice.action == "story":
                self.mark_story(session)
            elif choice.action == "messages":
                core = MessageCore()
                return core.run()

    def __str__(self):
        """Return string representation of object."""
        return str(self._stable)
