from message import Message


class NewGame(Message):
    """ Message to indicate creation of a new game."""
    def __str__(self):
        return "New Game"
