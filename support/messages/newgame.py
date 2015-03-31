from message import Message


class NewGame(Message):
    """ Message to indicate creation of a new game."""
    def __init__(self, name=False):
        self.name = name
    
    def __str__(self):
        return "New Game"
