"""Game logic for Main screen."""
from core import Core
from stablecore import StableCore
from towncore import TownCore
from pasturecore import PastureCore
from backend.stablebackend import StableBackend
from backend.pasturebackend import PastureBackend


class MainCore(Core):

    """Logic for Main game screen. Here you can pick a building to go to."""

    def __init__(self):
        """Set display."""
        Core.__init__(self)
        # self._display = MainDisplay()

    def get_actions(self, session):
        """Return actions for display."""
        actions = [TownCore()]

        stables = StableBackend.all(session)
        for stable in stables:
            actions.append(StableCore(stable))

        pastures = PastureBackend.all(session)
        for pasture in pastures:
            actions.append(PastureCore(pasture))

        return actions

    def choice(self, session, choice):
        """Handle user choice."""
        result = Core.choice(self, session, choice)
        if result == "handled":
            return None
        elif result is None:
            # Normally, this would mean a non-standard choice, to be handled
            # by this class. However, there are no non-standard choices in
            # this case.
            return None
        else:
            return result

    def __str__(self):
        """Return string representation of object."""
        return "Main"
