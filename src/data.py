"""
Custom data types.
"""


import logging

from datetime import datetime as dt


class Timeline(object):
    """Base class that represent the interface for a timeline."""

    #def get_events(self, start_time, end_time):
    #    """Return all events visible within the time period."""
    #    pass

    def get_events(self, time_period):
        return [e for e in self.events if e.inside_period(time_period)]

    #def preferred_period(self):
    #    """Return the preferred period to display of this timeline."""
    #    pass

    def preferred_period(self):
        return TimePeriod(dt(2008, 11, 1), dt(2008, 11, 30))


class Event(object):

    def __init__(self, start_time, end_time, text):
        self.time_period = TimePeriod(start_time, end_time)
        self.text = text

    def inside_period(self, time_period):
        return self.time_period.overlap(time_period)

    def is_period(self):
        return self.time_period.is_period()


class TimePeriod(object):

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        if start_time > end_time:
            raise Exception("Invalid time period")

    def inside(self, time):
        return time >= self.start_time and time <= self.end_time

    def overlap(self, time_period):
        return time_period.inside(self.start_time) or \
               time_period.inside(self.end_time)

    def is_period(self):
        return self.start_time != self.end_time

    def zoom(self, times):
        delta = times * self.delta() / 10
        self.start_time += delta
        self.end_time -= delta

    def delta(self):
        return self.end_time - self.start_time
