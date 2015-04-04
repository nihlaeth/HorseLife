from display import Display


class TownDisplay(Display):
    def __init__(self):
        Display.__init__(self)
        self._title = "Town"
        self._description = ("Welcome to the town center!")
