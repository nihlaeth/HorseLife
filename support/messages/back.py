from message import Message


class Back(Message):
    """ Message to indicate moving a level up in the hierarchy."""
    def __str__(self):
        return "Back"
