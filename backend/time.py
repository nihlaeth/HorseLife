"""Timekeeping mechanism."""
from operator import attrgetter
from enum import Enum

from settingbackend import SettingBackend
from horsebackend import HorseBackend
from stablebackend import StableBackend
from eventbackend import EventBackend
from support.messages.timestamp import TimeStamp


# Simple enum to translate between index numbers and weekdays.
# Note: week starts on Monday(0). Also note the captialization.
DAY = Enum(
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saurday",
    "Sunday")


class Time(object):

    """Timekeeping mechanism."""

    def __init__(self, session):
        """Get the id's of the relevant settings."""
        self._time_id = SettingBackend.one(session, "Time").id_
        self._date_id = SettingBackend.one(session, "Date").id_

    def get_day(self, session):
        """Return day of the week."""
        date = SettingBackend(self._date_id)
        return DAY[date.get(session, None, "numeric") % 7]

    def get_time(self, session):
        """Deprecated -- use get_time_stamp."""
        time_ = SettingBackend(self._time_id)
        total_minutes = time_.get(session, None, "numeric")
        hours = total_minutes / 60
        minutes = total_minutes % 60
        return ":".join([
            str(hours) if hours > 9 else "0" + str(hours),
            str(minutes) if minutes > 9 else "0" + str(minutes)])

    def get_time_stamp(self, session):
        """Return TimeStamp object indicating current time.

        session -- sqlalchemy session
        """
        date = SettingBackend(self._date_id).get(session, None, "numeric")
        time_ = SettingBackend(self._time_id).get(session, None, "numeric")
        return TimeStamp(date, time_)

    def pass_time(self, session, now):
        """Pass the time and activate whatever event is passed in doing so.

        session -- sqlalchemy session
        now -- TimeStamp object set to the target time (the new now)
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
        SettingBackend.one(session, "Time").set(
            session,
            "numeric",
            now.time)
        SettingBackend.one(session, "Date").set(
            session,
            "numeric",
            now.date)

        # valid_classes = [HorseBackend, StableBackend]
        # valid_map = dict(((c.__name__, c) for c in validClasses))
        events = list(EventBackend.all_raw(session))
        horses_temp = HorseBackend.all_raw(session)
        # Now organize the horses for easy access.
        horses = {}
        for horse in horses_temp:
            horses[str(horse.mid)] = horse
        stables_temp = StableBackend.all_raw(session)
        stables = {}
        for stable in stables_temp:
            stables[str(stable.mid)] = stable

        self._process_events(now, events, stables, horses)

        if now.is_night():
            # It's between 22:00 and 07:00 - night time!
            # TODO emit some notification so the user gets feedback about
            # the date change!
            now.end_of_night()
            self.pass_time(session, now)

    # We know this could be a function, but it's definitely a part
    # of the timekeeping system, and a private one at that.
    # For the sake of encapsulation, we're keeping it this way.
    # pylint: disable=no-self-use
    def _process_events(self, now, events, stables, horses):
        """Do event callbacks, update timestamps, etc."""
        while events[0].t_stamp <= now:
            t_stamp = events[0].t_stamp
            callbacks = events[0].callbacks
            subject = events[0].subject
            for callback in callbacks:
                obj = callback.obj
                obj_id = callback.obj_id
                if obj == "StableBackend":
                    e_info = stables[str(obj_id)].event(
                        subject,
                        t_stamp,
                        night=True)
                elif obj == "HorseBackend":
                    e_info = horses[str(obj_id)].event(
                        subject,
                        t_stamp)
                # Update event
                events[0].update(e_info["t_stamp"])
            # Events will have changed timestamp by now
            events = sorted(
                events,
                key=attrgetter("date", "time"))
