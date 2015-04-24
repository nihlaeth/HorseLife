"""Meter message."""
from message import Message


class Meter(Message):

    """Signal the interface module to display a meter."""

    def __init__(self, percent):
        """Set percentage filled."""
        self.percent = percent

    def __str__(self):
        """Return string representation for object."""
        return ''.join([self.percent, "%"])
