"""Game logic for Town screen."""
from core import Core
from contractercore import ContracterCore
from support.messages.action import Action
from errors.invalidchoice import InvalidChoice


class TownCore(Core):

    """Game logic for Town screen.

    Town: anything not directly affiliated with the business we're
    running. Construction, education, horse market, competitions, etc.
    """

    def __init__(self):
        """Set display."""
        Core.__init__(self)

    def get_info(self, session):
        """Return info list."""
        info = Core.get_info(self, session)
        info.append("Where do you want to visit?")
        return info

    def get_actions(self, _):
        """Return action list."""
        return [
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

    # pylint: disable=arguments-differ
    def choice(self, session, choice):
        """Handle user choice."""
        result = Core.choice(self, session, choice)
        if result == "handled":
            return None
        elif result is None:
            if isinstance(choice, Action):
                if choice.action == "contracter":
                    return ContracterCore()
                else:
                    raise InvalidChoice(choice)
            else:
                raise InvalidChoice(choice)
        else:
            return result

    def __str__(self):
        """Return string representation of object."""
        return "Town"
