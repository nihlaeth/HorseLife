"""Game logic for contracter store."""
import ConfigParser

from interface.cli.contracterdisplay import ContracterDisplay
from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.command import Command
from support.messages.action import Action
from backend.session import SessionScope
from backend.time import Time
from backend.stablebackend import StableBackend
from generators.stablegenerator import StableGenerator


class ContracterCore(Core):

    """Game logic for contracter store.

    This handles ALL building (and destruction) in the game,
    except for initial construction when starting a new game.
    """

    def __init__(self):
        """Set display and screen."""
        Core.__init__(self)
        self._display = ContracterDisplay()
        self._screen = "home"

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                time = Time(session)
                now = time.get_time_stamp(session)
                info = [" ".join(["Time", time.get_time(session)])]

                if self._screen == "home":
                    info.append("What do you want constructed?")
                    actions = [
                        Action("stables", "Stables"),
                        Action("pastures", "Pastures"),
                        Action("arenas", "Arenas"),
                        Action("tack-feed", "Tack and feed rooms")]
                elif self._screen == "stables":
                    actions = []
                    config = ConfigParser.SafeConfigParser()
                    config.read("config/stables.cfg")
                    for section in config.sections():
                        info.append("")
                        info.append(section)
                        info.append(config.get(section, "description"))
                        info.append(" ".join([
                            "Surface:",
                            config.get(section, "surface")]))
                        info.append(" ".join([
                            "Outside surface:",
                            config.get(section, "outside_surface")]))
                        info.append(" ".join([
                            "Light:",
                            config.get(section, "light")]))
                        info.append(" ".join([
                            "Capacity:",
                            config.get(section, "capacity")]))
                        info.append(" ".join([
                            "Base rent:",
                            config.get(section, "rent")]))
                        info.append(" ".join([
                            "Price:",
                            config.get(section, "price")]))
                        actions.append(Action("buy-stable",
                                              " ".join([
                                                  "Buy",
                                                  section,
                                                  "for",
                                                  config.get(
                                                      section,
                                                      "price")]),
                                              [section]))
                    actions.append(Action("home",
                                          "Look at other building types"))
                menu = [Back(), Quit()]

                self._display.init(actions, menu, info)
                choice = self._display.display()
                if isinstance(choice, Quit) or isinstance(choice, Back):
                    return choice
                elif isinstance(choice, Command):
                    exec(choice.command)
                elif isinstance(choice, Action):
                    if choice.action in [
                            "home",
                            "stables",
                            "pastures",
                            "arenas",
                            "tack-feed"]:
                        self._screen = choice.action
                    if choice.action == "buy-stable":
                        # TODO once you have money implemented, check if
                        # you have enough cash and decrease it with the
                        # price.
                        stable_id = StableGenerator().gen_many(
                            session,
                            1,
                            choice.arguments[0],
                            now)[0].id
                        stable = StableBackend(stable_id)
                        stable.get_events(session, now)

                session.commit()

    def __str__(self):
        """Return string representation of object."""
        return "Contracter"
