"""
Custom data types.
"""


import logging

from datetime import datetime as dt


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
        delta = times * self.delta() / 10
        self.start_time += delta
        self.end_time -= delta

    def delta(self):
        return self.end_time - self.start_time
