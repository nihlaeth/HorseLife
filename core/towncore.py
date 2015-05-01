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
                story = self.get_story(session)
                self._display.init(actions, menu, info, story)
                choice = self._display.display()
                if debug():
                    pdb.set_trace()
                result = None
                if isinstance(choice, Quit) or isinstance(choice, Back):
                    return choice
                elif isinstance(choice, Action):
                    if choice.action == "contracter":
                        result = ContracterCore().run()
                    elif choice.action == "story":
                        self.mark_story(session)
                    elif choice.action == "messages":
                        core = MessageCore()
                        result = core.run()

                if isinstance(result, Quit):
                    return result
                session.commit()

    def __str__(self):
        """Return string representation of object."""
        return "Town"
