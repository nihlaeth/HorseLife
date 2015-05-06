"""Game logic for contracter store."""
import ConfigParser
import pdb

from support.debug import debug
from interface.cli.contracterdisplay import ContracterDisplay
from core import Core
from messagecore import MessageCore
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.action import Action
from backend.session import SessionScope
from backend.time import Time
from backend.stablebackend import StableBackend
from backend.personbackend import PersonBackend
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
        self._msg = None

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                time = Time(session)
                now = time.get_time_stamp(session)
                info = self._info(session)

                if self._msg is not None:
                    info.append("")
                    info.append(self._msg)
                    info.append("")
                    self._msg = None

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
                        price = config.get(section, "price")
                        info.append(" ".join([
                            "Price:",
                            price]))
                        actions.append(Action("buy-stable",
                                              " ".join([
                                                  "Buy",
                                                  section,
                                                  "for",
                                                  price]),
                                              [section, price]))
                    actions.append(Action("home",
                                          "Look at other building types"))
                menu = [Back(), Quit()]

                story = self.get_story(session)
                self._display.init(actions, menu, info, story)
                choice = self._display.display()
                if debug():
                    pdb.set_trace()
                result = self._choice(session, choice, now)
                if isinstance(result, Quit) or isinstance(result, Back):
                    return result

    def _choice(self, session, choice, now):
        """Handle user choice."""
        if isinstance(choice, Quit):
            return choice
        if isinstance(choice, Back):
            if self._screen != "home":
                self._screen = "home"
            else:
                return choice
        elif isinstance(choice, Action):
            if choice.action in [
                    "home",
                    "stables",
                    "pastures",
                    "arenas",
                    "tack-feed"]:
                self._screen = choice.action
            elif choice.action == "buy-stable":
                person = PersonBackend.active_player(session)
                transaction = {
                    "subject": "Buy %s at contracter" % choice.arguments[0],
                    "t_stamp": now,
                    "amount": int(choice.arguments[1])}
                if person.spend_money(session, transaction):
                    stable_id = StableGenerator().gen_many(
                        session,
                        1,
                        choice.arguments[0],
                        now)[0].mid
                    stable = StableBackend(session, stable_id)
                    stable.get_events(session, now)
                    self._msg = "You successfully bought a stable!"
                else:
                    self._msg = "You don't have enough money for that!"
            elif choice.action == "story":
                self.mark_story(session, now)
            elif choice.action == "messages":
                core = MessageCore()
                result = core.run()
                if isinstance(result, Quit):
                    return result

    def __str__(self):
        """Return string representation of object."""
        return "Contracter"
