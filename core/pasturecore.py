"""Game logic for Pasture screen."""
from core import Core
from support.messages.meter import Meter
from support.messages.action import Action
from backend.horsebackend import HorseBackend
from backend.time import Time
from errors.invalidchoice import InvalidChoice


class PastureCore(Core):

    """Game logic for Pasture screen.

    View a pasture (and it's inhabitants). This is the main starting
    point for doing anything with a horse.
    """

    def __init__(self, pasture):
        """Get display and set pasture and horse private attributes.

        pasture -- PastureBackend instance
        """
        Core.__init__(self)
        self._pasture = pasture

    def get_info(self, session):
        """Return info list."""
        time = Time(session)
        now = time.get_time_stamp(session)
        info = Core.get_info(self, session)
        info.append("")
        info.append("Cleanliness:")
        info.append(Meter(self._pasture.get(
            session,
            now,
            "cleanliness")))
        return info

    def get_actions(self, session):
        """Return action list."""
        horses = self._pasture.get(session, None, "horses")
        actions = []
        for horse in horses:
            actions.append(Action(
                "stable",
                "Bring %s to the stable." % horse.name,
                [HorseBackend(session, horse.mid)]))

        actions.append(Action("clean", "Clean pasture"))
        return actions

    # pylint: disable=arguments-differ
    def choice(self, session, choice):
        """Handle user choice."""
        time = Time(session)
        now = time.get_time_stamp(session)
        result = Core.choice(self, session, choice)
        if result == "handled":
            return None
        elif result is None:
            if isinstance(choice, Action):
                if choice.action == "clean":
                    new_time = self._pasture.clean(session, now)
                    time.pass_time(session, new_time)
                elif choice.action == "stable":
                    horse = choice.arguments[0]
                    self._pasture.remove_horse(session, horse)
            else:
                raise InvalidChoice(choice)
        else:
            return result

    def __str__(self):
        """Return string representation of object."""
        return str(self._pasture)
