from display import Display


class LoadDisplay(Display):
    def __init__(self):
        Display.__init__(self)
        self._title = "Select game"
        self._description = (
                "Welcome to HorseLife!\n\n"
                "Select an existing game below, or create a new game.")
