from message import Message


class Event(Message):
    """ Signal the interface module to display a meter."""
    def __init__(self, date, time, callback):
        self.date = date
        self.time = time
        self.callback = callback

    def __str__(self):
        return ' '.join(["Event: Date:",
                         str(self.date),
                         "Time:",
                         str(self.time),
                         str(self.callback)])

    def __eq__(self, other):
        if other is None:
            return False
        if self.date == other.date and self.time == other.time:
            return True
        return False

    def __ne__(self, other):
        if other is None:
            return True
        if self.date == other.date and self.time == other.time:
            return False
        return True

    def __lt__(self, other):
        if other is None:
            return False
        if self.date < other.date:
            return True
        elif self.date == other.date and self.time < other.time:
            return True
        return False

    def __le__(self, other):
        if other is None:
            return False
        if self.date < other.date:
            return True
        elif self.date == other.date and self.time <= other.time:
            return True
        return False

    def __gt__(self, other):
        if other is None:
            return False
        if self.date > other.date:
            return True
        elif self.date == other.date and self.time > other.time:
            return True
        return False

    def __ge__(self, other):
        if other is None:
            return False
        if self.date > other.date:
            return True
        elif self.date == other.date and self.time >= other.time:
            return True
        return False
