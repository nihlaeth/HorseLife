"""TimeStamp message."""
from enum import Enum
from message import Message


DAY = Enum(
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday")


class TimeStamp(Message):

    """Holds a time and date and does basic math with those."""

    def __init__(self, date, time):
        """Set date and time."""
        self.date = int(date)
        self.time = int(time)

    def get_min(self):
        """Return the date/time as total amount of minutes (int)."""
        return self.time + self.date * 1440

    def add_min(self, minutes):
        """Add minutes to date/time."""
        self.time += int(minutes)
        if self.time >= 1440:
            self.date += self.time / 1440
            self.time %= 1440
        return self

    def get_str_day(self):
        """Return string representation of the date (day of week)."""
        return DAY[self.date % 7]

    def get_str_time(self):
        """Return string representation of the time (24h format)."""
        hours = self.time / 60
        minutes = self.time % 60
        return ":".join([
            str(hours) if hours > 9 else "0" + str(hours),
            str(minutes) if minutes > 9 else "0" + str(minutes)])

    def end_of_night(self, event=False):
        """Skip self to the end of the night."""
        if self.time >= 1320:
            self.date += 1
        if event:
            if self.time == 419:
                # Came here after putting time at
                # a minute before the transition.
                self.time = 420
                self.start_of_night(event=True)
                return None
            # Just before the transition, so night dependent needs will
            # compute correctly.
            self.time = 419
        else:
            self.time = 420

    def start_of_night(self, event=False):
        """Skip self to the start of the night."""
        if self.time > 1320:
            self.date += 1
        if event:
            if self.time == 1319:
                # Came here after putting time at
                # a minute before the transition.
                self.time = 1320
                self.end_of_night(event=True)
                return None
            # Just before the transition, so night-dependent needs will
            # compute correctly.
            self.time = 1319
        else:
            self.time = 1320

    def is_night(self):
        """Check if it's night (bool)."""
        if self.time >= 1320 or self.time < 420:
            return True
        else:
            return False

    def __repr__(self):
        """Return raw data."""
        return " ".join([
            "Timestamp: Date:",
            str(self.date),
            "Time:",
            str(self.time)])

    def __str__(self):
        """Return string representation of object."""
        return ' '.join([
            str(self.get_str_day()),
            str(self.date),
            self.get_str_time()])

    def __eq__(self, other):
        """Operator ==."""
        if self.date == other.date and self.time == other.time:
            return True
        return False

    def __ne__(self, other):
        """Operator !=."""
        if self.date == other.date and self.time == other.time:
            return False
        return True

    def __lt__(self, other):
        """Operator <."""
        if self.date < other.date:
            return True
        elif self.date == other.date and self.time < other.time:
            return True
        return False

    def __le__(self, other):
        """Operator <=."""
        if self.date < other.date:
            return True
        elif self.date == other.date and self.time <= other.time:
            return True
        return False

    def __gt__(self, other):
        """Operator >."""
        if self.date > other.date:
            return True
        elif self.date == other.date and self.time > other.time:
            return True
        return False

    def __ge__(self, other):
        """Operator >=."""
        if self.date > other.date:
            return True
        elif self.date == other.date and self.time >= other.time:
            return True
        return False

    def __add__(self, other):
        """Operator +."""
        date = self.date + other.date
        time = self.time + other.time
        if time >= 1440:
            date += time / 1440
            time %= 1440
        return TimeStamp(date, time)

    def __sub__(self, other):
        """Operator -."""
        date = self.date - other.date
        time = self.time - other.time
        if time < 0:
            date += time / 1440
            time %= 1440
        return TimeStamp(date, time)

    def __mul__(self, other):
        """When multiplying, this object behaves as a simple integer.

        (total amount of minutes)
        """
        return (self.time + 60 * self.date) * other

    def __div__(self, other):
        """When dividing, this object behaves as a simple integer.

        (total amount of minutes)
        """
        return (self.time + 60 * self.date) / other
