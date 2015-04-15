from operator import attrgetter
from enum import Enum
from sqlalchemy import inspect

from session import session_scope
from settingbackend import SettingBackend
from horsebackend import HorseBackend
from stablebackend import StableBackend
from eventbackend import EventBackend
from support.messages.timestamp import TimeStamp


""" Simple enum to translate between index numbers and weekdays.
Note: week starts on Monday(0). Also note the captialization."""
day = Enum(
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saurday",
    "Sunday")


class Time():
    def get_day(self, session):
        """ Deprecated -- use get_time_stamp"""
        self._date = SettingBackend.one(session, "Date")
        return day[self._date.get(session, "numeric") % 7]

    def get_time(self, session):
        """ Deprecated -- use get_time_stamp"""
        self._time = SettingBackend.one(session, "Time")
        hours = self._time.get(session, "numeric") / 60
        minutes = self._time.get(session, "numeric") % 60
        return ":".join([
                str(hours) if hours > 9 else "0" + str(hours),
                str(minutes) if minutes > 9 else "0" + str(minutes)])

    def get_time_stamp(self, session):
        """ Return TimeStamp object indicating current time.

        session -- sqlalchemy session
        """
        date = SettingBackend.one(session, "Date").get(session, "numeric")
        time = SettingBackend.one(session, "Time").get(session, "numeric")
        return TimeStamp(date, time)

    def pass_time(self, session, minutes, night=False):
        """ Pass the time and activate whatever event is passed in doing so.

        session -- sqlalchemy session
        minutes -- minutes to pass (int) --> to be replaced by a TimeStamp
            object to allow for easier calculations
        night -- indicates resting time, only if there are no actions
            being performed by the player (bool)

        Note: pass_time has limited to no knowledge of what happens with
        events. It just receives them, checks if they are within the
        time range, and if so, calls the callbacks. It does not receive
        any returns, the backends take care of their own side effects
        (like updating events). It might be better to move that
        to the pass_time method in the future (it would allow the
        EventBackend to inherit from Backend again).
        """
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
        events = EventBackend.all_raw(session)
        horses_temp = HorseBackend.all_raw(session)
        # Now organize the horses for easy access.
        horses = {}
        for horse in horses_temp:
            horses[str(horse.id)] = horse
        stables_temp = StableBackend.all_raw(session)
        stables = {}
        for stable in stables_temp:
            stables[str(stable.id)] = stable
        while events[0].t_stamp <= now:
            t_stamp = events[0].t_stamp
            callbacks = events[0].callbacks
            subject = events[0].subject
            for callback in callbacks:
                obj = callback.obj
                obj_id = callback.obj_id
                cls = validMap[obj]
                if obj == "StableBackend":
                    e_info = stables[str(obj_id)].event(subject, t_stamp)
                elif obj == "HorseBackend":
                    e_info = horses[str(obj_id)].event(subject, t_stamp)
                # Update event
                events[0].update(e_info["t_stamp"])
            # Events will have changed timestamp by now
            events = sorted(
                    events,
                    key=attrgetter("date", "time"))

        if time >= 1320 or time < 420:
            # It's between 22:00 and 07:00 - night time!
            # If you managed to get past midnight, you're seriously
            # depriving your horses of sleep...
            # TODO emit some notification so the user gets feedback about
            # the date change!
            if time >= 1320:
                minutes_to_pass = 420 + 1440 - time
            else:
                minutes_to_pass = 420 - time
            self.pass_time(session, minutes_to_pass, True)

time = Time()
