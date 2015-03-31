from message import Message


class Quit(Message):
    """ Message to indicate shutdown."""
    def __str__(self):
        return "Save and Quit"
