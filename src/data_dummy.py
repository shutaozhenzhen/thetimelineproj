"""
Implementation of a Dummy Timeline that has a static storage
"""


import logging

from datetime import datetime as dt

from data import Timeline
from data import Event


class DummyTimeline(Timeline):
    """Timeline with dummy data for testing purposes."""

    def __init__(self):
        self.events = [
            Event(dt(2008, 11, 22), dt(2008, 11, 22), "Foo"),
            Event(dt(2008, 11, 19), dt(2008, 11, 19), "Bar"),
            Event(dt(2008, 11, 5), dt(2008, 11, 15), "Foobar"),
        ]
