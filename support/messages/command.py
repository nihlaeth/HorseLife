from message import Message


class Command(Message):
    """ Signal the interface module to display a meter."""
    def __init__(self, command):
        self.command = command

    def __str__(self):
        return ' '.join(["Command:", self.command])
