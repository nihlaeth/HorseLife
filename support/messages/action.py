from message import Message


class Action(Message):
    """ Container for actions, for example clean a stable, groom a horse."""
    def __init__(self, action, description, arguments=[]):
        self.action = action
        self.description = description
        self.arguments = arguments

    def __str__(self):
        return self.description
