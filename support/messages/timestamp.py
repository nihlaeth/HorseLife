from message import Message


class TimeStamp(Message):
    """ Signal the interface module to display a meter."""
    def __init__(self, date, time):
        self.date = int(date)
        self.time = int(time)

    def get_min(self):
        return self.time + self.date * 60

    def add_min(self, minutes):
        self.time += int(minutes)
        if self.time >= 1440:
            self.date += self.time / 1440
            self.time %= 1440

    def __str__(self):
        return ' '.join(["Timestamp: Date:",
                         str(self.date),
                         "Time:",
                         str(self.time)])

    def __eq__(self, other):
        if self.date == other.date and self.time == other.time:
            return True
        return False

    def __ne__(self, other):
        if self.date == other.date and self.time == other.time:
            return False
        return True

    def __lt__(self, other):
        if self.date < other.date:
            return True
        elif self.date == other.date and self.time < other.time:
            return True
        return False

    def __le__(self, other):
        if self.date < other.date:
            return True
        elif self.date == other.date and self.time <= other.time:
            return True
        return False

    def __gt__(self, other):
        if self.date > other.date:
            return True
        elif self.date == other.date and self.time > other.time:
            return True
        return False

    def __ge__(self, other):
        if self.date > other.date:
            return True
        elif self.date == other.date and self.time >= other.time:
            return True
        return False

    def __add__(self, other):
        date = self.date + other.date
        time = self.time + other.time
        if time >= 1440:
            date += time / 1440
            time %= 1440
        return TimeStamp(date, time)

    def __sub__(self, other):
        date = self.date - other.date
        time = self.time - other.time
        if time < 0:
            date += time / 1440
            time %= 1440
        return TimeStamp(date, time)

    def __mul__(self, other):
        """When multiplying, this object behaves as a simple integer.
        (total amount of minutes)"""
        return (self.time + 60 * self.date) * other

    def __div__(self, other):
        """When dividing, this object behaves as a simple integer.
        (total amount of minutes)"""
        return (self.time + 60 * self.date) / other