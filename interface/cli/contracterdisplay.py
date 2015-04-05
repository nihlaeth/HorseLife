from display import Display


class ContracterDisplay(Display):
    def __init__(self):
        Display.__init__(self)
        self._title = "Contracter"
        self._description = (
                "Welcome!\n"
                "If you need some construction done, "
                "You've come to the right place! We're "
                "extremely fast, and land costs are included "
                "in all our prices. Happy shopping!")
