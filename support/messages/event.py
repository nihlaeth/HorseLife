from message import Message
from timestamp import TimeStamp


class Event(Message):
    """ Signal the interface module to display a meter."""
    def __init__(self, date, time, callback, subject, night=False):
        self.callback = callback
        self.subject = subject
        self.t_stamp = TimeStamp(date, time)
        self.night = night

    def __str__(self):
        return ' '.join(["Event: Date:",
                         str(self.t_stamp.date),
                         "Time:",
                         str(self.t_stamp.time),
                         str(self.callback)])

    def __eq__(self, other):
        if other is None:
            return False
        return self.t_stamp == other.t_stamp

    def __ne__(self, other):
        if other is None:
            return True
        return self.t_stamp != other.t_stamp

    def __lt__(self, other):
        if other is None:
            return False
        return self.t_stamp < other.t_stamp

    def __le__(self, other):
        if other is None:
            return False
        return self.t_stamp <= other.t_stamp

    def __gt__(self, other):
        if other is None:
            return False
        return self.t_stamp > other.t_stamp

    def __ge__(self, other):
        if other is None:
            return False
        return self.t_stamp >= other.t_stamp
