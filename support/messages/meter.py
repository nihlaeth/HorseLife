from message import Message


class Meter(Message):
    """ Signal the interface module to display a meter."""
    def __init__(self, percent):
        self.percent = percent

    def __str__(self):
        return ''.join([self.percent, "%"])
