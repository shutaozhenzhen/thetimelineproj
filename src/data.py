"""
Custom data types.
"""


import logging

from datetime import datetime as dt
from datetime import timedelta


class Timeline(object):
    """Base class that represent the interface for a timeline."""

    def get_events(self, start_time, end_time):
        """Return all events visible within the time period."""
        pass

    def preferred_period(self):
        """Return the preferred period to display of this timeline."""
        pass

    def new_event(self, event):
        """Add a new event to the Timeline"""
        pass


class Event(object):
    """Represents one event on a timeline."""

    def __init__(self, start_time, end_time, text):
        """start_time and end_time shall be of the type datetime"""
        self.time_period = TimePeriod(start_time, end_time)
        self.text = text

    def inside_period(self, time_period):
        return self.time_period.overlap(time_period)

    def is_period(self):
        return self.time_period.is_period()

    def mean_time(self):
        return self.time_period.mean_time()


class TimePeriod(object):
    """
    """

    MAX_DIFF = timedelta(120 * 365) # 120 years
    MIN_DIFF = timedelta(hours=1) # 1 hour

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        if start_time > end_time:
            raise Exception("Invalid time period")

    def inside(self, time):
        return time >= self.start_time and time <= self.end_time

    def overlap(self, time_period):
        return not (time_period.end_time < self.start_time and \
                    time_period.start_time > self.end_time)

    def is_period(self):
        return self.start_time != self.end_time

    def mean_time(self):
        return self.start_time + self.delta() / 2

    def zoom(self, times):
        delta = mult_timedelta(self.delta(), times / 10.0)
        self.start_time += delta
        self.end_time -= delta
        if self.delta() > TimePeriod.MAX_DIFF:
            foo = (self.delta() - TimePeriod.MAX_DIFF) / 2
            self.start_time += foo
            self.end_time -= foo
        elif self.delta() < TimePeriod.MIN_DIFF:
            foo = (TimePeriod.MIN_DIFF - self.delta()) / 2
            self.start_time -= foo
            self.end_time += foo

    def move(self, dir):
        delta = mult_timedelta(self.delta(), dir / 10.0)
        self.start_time += delta
        self.end_time += delta

    def delta(self):
        return self.end_time - self.start_time


def mult_timedelta(td, num):
    """Calculate a new timedelta that is `num` times larger than `td`."""
    days = td.days * num
    seconds = td.seconds * num
    microseconds = td.microseconds * num
    return timedelta(days, seconds, microseconds)


def div_timedeltas(td1, td2):
    """Calculate how many times td2 fit in td1."""
    # Since Python can handle infinitely large numbers, this solution works. It
    # might however not be optimal. If you are clever, you should be able to
    # treat the different parts individually. But this is simple.
    us_per_sec = 1000000 
    us_per_day = 24 * 60 * 60 * us_per_sec
    total_us1 = (td1.days * us_per_day + td1.seconds * us_per_sec +
                 td1.microseconds)
    total_us2 = (td2.days * us_per_day + td2.seconds * us_per_sec +
                 td2.microseconds)
    # Make sure that the result is a floating point number
    return total_us1 / float(total_us2)
