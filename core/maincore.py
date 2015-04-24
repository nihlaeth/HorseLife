"""Game logic for Main screen."""
from interface.cli.maindisplay import MainDisplay
from core import Core
from buildingcore import BuildingCore
from towncore import TownCore
from support.messages.quit import Quit
from support.messages.command import Command
from backend.session import SessionScope
from backend.stablebackend import StableBackend
from backend.time import Time


class MainCore(Core):

    """Logic for Main game screen. Here you can pick a building to go to."""

    def __init__(self):
        """Set display."""
        Core.__init__(self)
        self._display = MainDisplay()

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                stables = StableBackend.all(session)

                info = [" ".join(["Time", Time(session).get_time(session)])]

                actions = [TownCore()]
                for stable in stables:
                    actions.append(BuildingCore(stable))

                menu = []
                menu.append(Quit())

                self._display.init(actions, menu, info)
                choice = self._display.display()
                if isinstance(choice, Quit):
                    return choice
                elif isinstance(choice, BuildingCore):
                    result = choice.run()
                elif isinstance(choice, TownCore):
                    result = choice.run()
                elif isinstance(choice, Command):
                    exec(choice.command)
                    result = None

                if result is not None:
                    if isinstance(result, Quit):
                        return result
                    # if it's of type Back, just display
                    # this screen again - continue loop.
                session.commit()

    def __str__(self):
        """Return string representation of object."""
        return "Main"
