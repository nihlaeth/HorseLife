"""Game logic for Message screen."""
from interface.cli.messagedisplay import MessageDisplay
from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from support.messages.command import Command
from support.messages.action import Action
from support.messages.timestamp import TimeStamp
from backend.session import SessionScope
from backend.messagebackend import MessageBackend


class MessageCore(Core):

    """Logic for Message screen."""

    def __init__(self):
        """Set display."""
        Core.__init__(self)
        self._display = MessageDisplay()
        self._screen = "list"
        self._message = None

    def run(self):
        """Run with it."""
        while True:
            with SessionScope() as session:
                messages = MessageBackend.all(session)

                info = self._info(session)

                actions = []

                if self._screen == "list":
                    for message in messages:
                        actions.append(Action(
                            "message",
                            str(message),
                            [message.id_]))
                elif self._screen == "message":
                    info.append("")
                    info.append(self._message.get(session, None, "subject"))
                    info.append("")
                    info.append(TimeStamp(
                        self._message.get(session, None, "date"),
                        self._message.get(session, None, "time")))
                    info.append("")
                    info.append(self._message.get(session, None, "text"))
                    actions.append(Action("delete", "Delete message"))
                    actions.append(Action("mark-unread", "Mark unread"))

                menu = [Back(), Quit()]
                story = self.get_story(session)
                self._display.init(actions, menu, info, story)

                choice = self._display.display()
                if isinstance(choice, Quit):
                    return choice
                elif isinstance(choice, Back):
                    if self._screen != "list":
                        self._screen = "list"
                    else:
                        return choice
                elif isinstance(choice, Command):
                    exec(choice.command)
                elif isinstance(choice, Action):
                    if choice.action == "message":
                        self._screen = "message"
                        self._message = MessageBackend(choice.arguments[0])
                    elif choice.action == "delete":
                        # TODO: implement delete - needs a backend method
                        pass

                    # Figure out if this message needs to be marked as read
                    if choice.action == "mark-unread":
                        self._message.set(session, "read", False)
                    else:
                        self._message.set(session, "read", True)

    def __str__(self):
        """Return string representation for object."""
        return "View messages"
