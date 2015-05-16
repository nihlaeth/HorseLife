"""Game logic for Message screen."""
from core import Core
from support.messages.action import Action
from support.messages.timestamp import TimeStamp
from support.messages.back import Back
from backend.messagebackend import MessageBackend
from errors.invalidchoice import InvalidChoice


class MessageCore(Core):

    """Logic for Message screen."""

    def __init__(self, message=None):
        """Set display."""
        Core.__init__(self)
        self._message = message

    def get_actions(self, session):
        """Return action list."""
        messages = MessageBackend.all(session)

        actions = []

        if self._message is None:
            for message in messages:
                actions.append(MessageCore(message))
        else:
            actions.append(Action("delete", "Delete message"))
            actions.append(Action("mark-unread", "Mark unread"))
        return actions

    def get_info(self, session):
        """Return info list."""
        info = Core.get_info(self, session)
        if self._message is not None:
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
        result = Core.choice(self, session, choice)
        if result == "handled":
            return None
        elif result is None:
            if isinstance(choice, Action):
                if choice.action == "delete":
                    self._message.delete(session)
                    return Back()
                elif choice.action != "mark-unread":
                    raise InvalidChoice(choice)

                # Figure out if this message needs to be marked as read
                if choice.action == "mark-unread":
                    self._message.set(session, "read", False)
                elif choice.action != "delete":
                    self._message.set(session, "read", True)
            else:
                raise InvalidChoice(choice)
        else:
            return result

    def __str__(self):
        """Return string representation for object."""
        if self._message is None:
            return "View messages"
        else:
            return str(self._message)
