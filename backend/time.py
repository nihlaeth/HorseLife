from operator import attrgetter
from enum import Enum
from sqlalchemy import inspect

from session import session_scope
from settingbackend import SettingBackend
from horsebackend import HorseBackend
from stablebackend import StableBackend
from eventbackend import EventBackend
from support.messages.timestamp import TimeStamp


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
        self._events = []

    def get_day(self, session):
        self._date = SettingBackend.one(session, "Date")
        return day[self._date.get(session, "numeric") % 7]

    def get_time(self, session):
        self._time = SettingBackend.one(session, "Time")
        hours = self._time.get(session, "numeric") / 60
        minutes = self._time.get(session, "numeric") % 60
        return ":".join([
                str(hours) if hours > 9 else "0" + str(hours),
                str(minutes) if minutes > 9 else "0" + str(minutes)])

    def get_time_stamp(self, session):
        date = SettingBackend.one(session, "Date").get(session, "numeric")
        time = SettingBackend.one(session, "Time").get(session, "numeric")
        return TimeStamp(date, time)

    def pass_time(self, session, minutes, night=False):
        if minutes == 0:
            return True
        time_obj = SettingBackend.one(session, "Time")
        date_obj = SettingBackend.one(session, "Date")
        time = time_obj.get(session, "numeric")
        date = date_obj.get(session, "numeric")

        time += minutes
        if time >= 1440:
            time -= 1440
            date += 1
        time_obj.set(session, "numeric", time)
        date_obj.set(session, "numeric", date)

        now = self.get_time_stamp(session)
        validClasses = [HorseBackend, StableBackend]
        validMap = dict(((c.__name__, c) for c in validClasses))
        while True:
            try:
                event = EventBackend.next_event(session)
            except IndexError:
                break
            t_stamp = event.get(session, "t_stamp")
            if t_stamp <= now:
                callbacks = event.get(session, "callbacks")
                subject = event.get(session, "subject")
                for callback in callbacks:
                    obj = callback.obj
                    obj_id = callback.obj_id
                    cls = validMap[obj]
                    cls(obj_id).event_callback(session, subject, t_stamp)
            else:
                break

        if time >= 1320 or time < 420:
            # It's between 22:00 and 07:00 - night time!
            # If you managed to get past midnight, you're seriously
            # depriving your horses of sleep...
            # TODO emit some event so the user gets feedback about
            # the date change!
            if time >= 1320:
                minutes_to_pass = 420 + 1440 - time
            else:
                minutes_to_pass = 420 - time
            self.pass_time(session, minutes_to_pass, True)

time = Time()
