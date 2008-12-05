"""
Implementation of a Dummy Timeline that has a static storage
"""


import logging

from datetime import datetime as dt

from data import Timeline
from data import TimePeriod
from data import Event


class DummyTimeline(Timeline):
    """Timeline with dummy data for testing purposes."""

    def __init__(self):
        self.events = [
            Event(dt(2008, 11, 22), dt(2008, 11, 22), "Foo"),
            Event(dt(2008, 11, 19, 13, 30, 0), dt(2008, 11, 19, 13, 30, 0), "Bar"),
            Event(dt(2008, 11, 5), dt(2008, 11, 15), "Foobar"),
        ]

    def get_events(self, time_period):
        return [e for e in self.events if e.inside_period(time_period)]

    def preferred_period(self):
        return TimePeriod(dt(2008, 11, 1), dt(2008, 11, 30))
