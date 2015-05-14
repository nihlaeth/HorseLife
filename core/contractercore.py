"""Game logic for contracter store."""
import ConfigParser

from core import Core
from support.messages.back import Back
from support.messages.action import Action
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
        self._screen = "home"

    def get_info(self, session):
        """Return information block."""
        info = Core.get_info(self, session)

        if self._screen == "home":
            info.append("What do you want constructed?")
        elif self._screen == "stables":
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
        return info

    def get_actions(self, _):
        """Return action block."""
        if self._screen == "home":
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
                price = config.get(section, "price")
                actions.append(Action("buy-stable",
                                      " ".join([
                                          "Buy",
                                          section,
                                          "for",
                                          price]),
                                      [section, price]))
            actions.append(Action("home", "Look at other building types"))
        return actions

    # pylint: disable=arguments-differ
    def choice(self, session, choice):
        """Handle user choice."""
        time = Time(session)
        now = time.get_time_stamp(session)
        result = Core.choice(self, session, choice, noback=True)
        if result == "handled":
            return None
        elif result is None:
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
                    subject = "Buy %s at contracter" % choice.arguments[0]
                    transaction = {
                        "subject": subject,
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
            else:
                return result

    def __str__(self):
        """Return string representation of object."""
        return "Contracter"
