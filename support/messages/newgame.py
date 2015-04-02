from message import Message


class NewGame(Message):
    """ Message to indicate creation of a new game."""
    def __init__(self, file_name=False):
        self.file_name = file_name

    def __str__(self):
        return "New Game"
