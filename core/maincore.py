"""Game logic for Main screen."""
from core import Core
from stablecore import StableCore
from towncore import TownCore
from pasturecore import PastureCore
from messagecore import MessageCore
from support.messages.quit import Quit
from support.messages.action import Action
from backend.time import Time
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
        if isinstance(choice, Quit):
            return choice
        elif isinstance(choice, Core):
            return choice
        elif isinstance(choice, Action):
            if choice.action == "story":
                self.mark_story(
                    session,
                    Time(session).get_time_stamp(session))
            if choice.action == "messages":
                return MessageCore()

    def __str__(self):
        """Return string representation of object."""
        return "Main"
