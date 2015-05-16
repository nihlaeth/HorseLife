"""Game logic for Message screen."""
from core import Core
from support.messages.back import Back
from support.messages.action import Action
from support.messages.timestamp import TimeStamp
from backend.messagebackend import MessageBackend


class MessageCore(Core):

    """Logic for Message screen."""

    def __init__(self):
        """Set display."""
        Core.__init__(self)
        self._screen = "list"
        self._message = None

    def get_actions(self, session):
        """Return action list."""
        messages = MessageBackend.all(session)

        actions = []

        if self._screen == "list":
            for message in messages:
                actions.append(Action(
                    "message",
                    str(message),
                    [message.id_]))
        elif self._screen == "message":
            actions.append(Action("delete", "Delete message"))
            actions.append(Action("mark-unread", "Mark unread"))
        return actions

    def get_info(self, session):
        """Return info list."""
        info = Core.get_info(self, session)
        if self._screen == "message":
            info.append("")
            info.append(self._message.get(session, None, "subject"))
            info.append("")
            info.append(TimeStamp(
                self._message.get(session, None, "date"),
                self._message.get(session, None, "time")))
            info.append("")
            info.append(self._message.get(session, None, "text"))
        return info

    # pylint: disable=arguments-differ
    def choice(self, session, choice):
        """Handle user choice."""
        result = Core.choice(self, session, choice, noback=True)
        if result == "handled":
            return None
        elif result is None:
            if isinstance(choice, Back):
                if self._screen != "list":
                    self._screen = "list"
                else:
                    return choice
            elif isinstance(choice, Action):
                if choice.action == "message":
                    self._screen = "message"
                    self._message = MessageBackend(
                        session,
                        choice.arguments[0])
                elif choice.action == "delete":
                    self._message.delete(session)

                # Figure out if this message needs to be marked as read
                if choice.action == "mark-unread":
                    self._message.set(session, "read", False)
                elif choice.action != "delete":
                    self._message.set(session, "read", True)
        else:
            return result

    def __str__(self):
        """Return string representation for object."""
        return "View messages"
