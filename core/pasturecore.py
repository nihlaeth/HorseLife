"""Game logic for Pasture screen."""
import pdb

from core import Core
from messagecore import MessageCore
from support.debug import debug
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.meter import Meter
from support.messages.action import Action
# from interface.cli.pasturedisplay import PastureDisplay
from backend.session import SessionScope
from backend.horsebackend import HorseBackend
from backend.time import Time


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
        # self._display = PastureDisplay()
        self._display = None

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                # Get horses
                horses = self._pasture.get(session, None, "horses")

                time = Time(session)
                now = time.get_time_stamp(session)
                info = self._info(session)
                info.append("")
                info.append("Cleanliness:")
                info.append(Meter(self._pasture.get(
                    session,
                    now,
                    "cleanliness")))

                actions = []
                for horse in horses:
                    actions.append(Action(
                        "stable",
                        "Bring %s to the stable." % horse.name,
                        [HorseBackend(session, horse.mid)]))

                actions.append(Action("clean", "Clean pasture"))

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
                new_time = self._pasture.clean(session, now)
                time.pass_time(session, new_time)
            elif choice.action == "stable":
                horse = choice.arguments[0]
                self._pasture.remove_horse(session, horse)
            elif choice.action == "story":
                self.mark_story(session, now)
            elif choice.action == "messages":
                core = MessageCore()
                return core.run()

    def __str__(self):
        """Return string representation of object."""
        return str(self._pasture)
