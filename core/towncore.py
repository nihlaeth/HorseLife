"""Game logic for Town screen."""
import pdb

from interface.cli.towndisplay import TownDisplay
from core import Core
from contractercore import ContracterCore
from messagecore import MessageCore
from support.debug import debug
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.action import Action
from backend.session import SessionScope
from backend.time import Time


class TownCore(Core):

    """Game logic for Town screen.

    Town: anything not directly affiliated with the business we're
    running. Construction, education, horse market, competitions, etc.
    """

    def __init__(self):
        """Set display."""
        Core.__init__(self)
        self._display = TownDisplay()

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                info = self._info(session)
                info.append("Where do you want to visit?")

                actions = [
                    Action("bank", "Bank"),
                    Action("horses", "Horse market", level=5),
                    Action("contracter", "Contracter", level=5),
                    Action("tack", "Saddle maker"),
                    Action("food", "Horse supplies"),
                    Action("veterinarian", "Veterinarian"),
                    Action("farrier", "Farrier"),
                    Action(
                        "competitions",
                        "National equine sports association",
                        level=15),
                    Action(
                        "employment",
                        "Employment agency",
                        level=20),
                    Action("newspaper", "News agency", level=20),
                    Action("education", "College", level=25)]
                menu = [Back(), Quit()]
                story = self.get_story(session)
                self._display.init(actions, menu, info, story)
                choice = self._display.display(self._level.level(session))
                if debug():
                    pdb.set_trace()
                result = None
                if isinstance(choice, Quit) or isinstance(choice, Back):
                    return choice
                elif isinstance(choice, Action):
                    if choice.action == "contracter":
                        result = ContracterCore().run()
                    elif choice.action == "story":
                        self.mark_story(
                            session,
                            Time(session).get_time_stamp(session))
                    elif choice.action == "messages":
                        core = MessageCore()
                        result = core.run()

                if isinstance(result, Quit):
                    return result
                session.commit()

    def __str__(self):
        """Return string representation of object."""
        return "Town"
