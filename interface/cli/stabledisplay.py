"""Display for Stable screen."""
import pdb

from display import Display
from backend.session import SessionScope
from support.debug import debug
from support.messages.action import Action
from errors.invalidchoice import InvalidChoice


class StableDisplay(Display):

    """Display for Stable screen."""

    def __init__(self, core):
        """Set title and description."""
        Display.__init__(self)
        self._title = "Stable"
        # self._description = (
        #    "Welcome to the stable!\n\n"
        #    "Here you can groom your horse, "
        #    "take it for a ride, and check "
        #    "how it's doing.")
        self._description = ""
        self._core = core

    # pylint: disable=arguments-differ
    def display(self):
        """Do some displaying."""
        with SessionScope() as session:
            self.init(session)

            result = self._core.choice(session, self._choice)

            if debug():
                pdb.set_trace()

            try:
                return self.choice(result)
            except InvalidChoice:
                if isinstance(result, Action):
                    if result.action == "change name":
                        name = self.get_string(4, "Name: ")
                        self._core.change_name(session, name)
                        # TODO: figure out why this is needed...
                        session.commit()
                        return self.display()
                    else:
                        raise InvalidChoice(result)
                else:
                    raise InvalidChoice(result)
