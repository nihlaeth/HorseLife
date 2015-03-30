from display import Display


class Main(Display):
    def __init__(self):
        Display.__init__(self)
        self._title = "HorseLife"
        self._description = (
            "Welcome to HorseLife!\n\n"
            "Below is a list of buildings on your property. To enter one,"
            "type their associated number and hit enter!")
