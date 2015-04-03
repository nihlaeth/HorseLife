from enum import Enum
from sqlalchemy import inspect

from session import session_scope
from settingsbackend import SettingsBackend
from horsesbackend import HorsesBackend
from stablesbackend import StablesBackend


day = Enum(
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saurday",
    "Sunday")


class Time():
    def __init__(self):
        with session_scope() as session:
            self._date = SettingsBackend.one(session, "Date")
            self._time = SettingsBackend.one(session, "Time")

    def get_day(self):
        with session_scope() as session:
            self._date = SettingsBackend.one(session, "Date")
            return day[self._date.numeric % 7]

    def get_time(self):
        with session_scope() as session:
            self._time = SettingsBackend.one(session, "Time")
            hours = self._time.numeric / 60
            minutes = self._time.numeric % 60
            return ":".join([
                str(hours) if hours > 9 else "0" + str(hours),
                str(minutes) if minutes > 9 else "0" + str(minutes)])

    def pass_time(self, minutes, night=False):
        with session_scope() as session:
            horses = HorsesBackend.all(session)
            for horse in horses:
                horse.pass_time(minutes, night)

            stables = StablesBackend.all(session)
            for stable in stables:
                stable.pass_time(minutes, night)

            # TODO move session out of the *backend files and up one layer
            # to prevent expired objects and such
            self._date = SettingsBackend.one(session, "Date")
            self._time = SettingsBackend.one(session, "Time")

            self._time.numeric += minutes
            if self._time.numeric >= 1440:
                self._time.numeric -= 1440
                self._date.numeric += 1

            session.commit()
            if self._time.numeric >= 1320 or self._time.numeric < 420:
                # It's between 22:00 and 07:00 - night time!
                # If you managed to get past midnight, you're seriously
                # depriving your horses of sleep...
                # TODO emit some event so the user gets feedback about
                # the date change!
                if self._time.numeric >= 1320:
                    minutes_to_pass = 420 + 1440 - self._time.numeric
                else:
                    minutes_to_pass = 420 - self._time.numeric
                self.pass_time(minutes_to_pass, night=True)

time = Time()
