"""Game logic for Stable screen."""
from core import Core
from support.messages.meter import Meter
from support.messages.action import Action
# from interface.cli.stabledisplay import StableDisplay
from backend.horsebackend import HorseBackend
from backend.time import Time
from errors.invalidchoice import InvalidChoice


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
        # self._display = StableDisplay()
        self._display = None
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

    def get_info(self, session):
        """Return info block."""
        horses = self._stable.get(session, None, "horses")
        if len(horses) > 0 and self._horse is None:
            self._horse = HorseBackend(session, horses[0].mid)

        time = Time(session)
        now = time.get_time_stamp(session)
        info = Core.get_info(self, session)
        info.append("")
        info.append("Cleanliness:")
        info.append(Meter(self._stable.get(
            session,
            now,
            "cleanliness")))
        info.append("Food tray:")
        info.append(Meter(self._stable.get(session, now, "food")))
        info.append("Water bucket:")
        info.append(Meter(self._stable.get(session, now, "water")))

        if self._horse is not None:
            # Lists are passed by reference by default
            self._horse_info(session, info, now)

        return info

    def get_actions(self, session):
        """Return action list."""
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

        horses = self._stable.get(session, None, "horses")
        if len(horses) > 1:
            for horse in horses:
                if horse.id != self._horse.id_:
                    actions.append(Action(
                        "fetch",
                        ''.join(["Fetch ", horse.name]),
                        [HorseBackend(session, horse.id)]))

        return actions

    # pylint: disable=arguments-differ
    def choice(self, session, choice):
        """Handle user choice."""
        result = Core.choice(self, session, choice)
        if result == "handled":
            return None
        elif result is None:
            if isinstance(choice, Action):
                time = Time(session)
                now = time.get_time_stamp(session)
                if choice.action == "clean":
                    new_time = self._stable.clean(session, now)
                    time.pass_time(session, new_time)
                elif choice.action == "change name":
                    return choice
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
            else:
                raise InvalidChoice(choice)
        else:
            return result

    def change_name(self, session, name):
        """Change horse name."""
        self._horse.set(session, "name", name)

    def __str__(self):
        """Return string representation of object."""
        return str(self._stable)
