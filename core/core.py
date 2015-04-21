class Core():
    def __init__(self):
        """ Some basic initialization: get a display, save some id's of
        related objects, or their backends or something like that."""
        self._display = None

    def run(self):
        """ Game logic! Get data through backend and frontend (interface
        / user input), and do stuff with it! Communicate back to backend
        and front-end, well, you get the picture."""
        pass

    def __str__(self):
        return "Core"
