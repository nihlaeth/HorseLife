"""Timekeeping mechanism."""
from operator import attrgetter

from settingbackend import SettingBackend
from horsebackend import HorseBackend
from stablebackend import StableBackend
from pasturebackend import PastureBackend
from eventbackend import EventBackend
from support.messages.timestamp import TimeStamp
from generators.messagegenerator import MessageGenerator


class Time(object):

    """Timekeeping mechanism."""

    def __init__(self, session):
        """Get the id's of the relevant settings."""
        self._time_id = SettingBackend.one(session, "Time").id_
        self._date_id = SettingBackend.one(session, "Date").id_

    def get_time_stamp(self, session):
        """Return TimeStamp object indicating current time.

        session -- sqlalchemy session
        """
        date = SettingBackend(
            session,
            self._date_id).get(session, None, "numeric")
        time_ = SettingBackend(
            session,
            self._time_id).get(session, None, "numeric")
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

        pastures_temp = PastureBackend.all_raw(session)
        pastures = {}
        for pasture in pastures_temp:
            pastures[str(pasture.mid)] = pasture

        self._process_events(session, now, events, stables, pastures, horses)

        if now.is_night():
            # It's between 22:00 and 07:00 - night time!
            # TODO emit some notification so the user gets feedback about
            # the date change!
            now.end_of_night()
            self.pass_time(session, now)

    def _process_events(self, session, now, events, stables, pastures, horses):
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
                        t_stamp)
                elif obj == "PastureBackend":
                    e_info = pastures[str(obj_id)].event(
                        subject,
                        t_stamp)
                elif obj == "HorseBackend":
                    e_info = horses[str(obj_id)].event(
                        subject,
                        t_stamp)
                # Update event
                events[0].update(e_info["t_stamp"])
                if e_info["msg"] is not None:
                    MessageGenerator.gen_many(session, [e_info["msg"]])
            # Events will have changed timestamp by now
            events = sorted(
                events,
                key=attrgetter("date", "time"))
