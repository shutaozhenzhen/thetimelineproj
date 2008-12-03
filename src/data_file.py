"""
Implementation of a Timeline that has a file storage
"""


import logging

from datetime import datetime as dt

from data import Timeline
from data import TimePeriod
from data import Event


class FileTimeline(Timeline):
    """Timeline with file storage."""

    def __init__(self, data_source):
        """Load events from data in the given file, data_source."""
        self.events = []
        f = open(data_source)
        try:
            try:
                for line in f:
                    self._create_and_add_event(line.strip())
            except Exception, e:
                logging.fatal('Error when reading file ' + data_source,
                              exc_info=e)
        finally:
            f.close()

    def _create_and_add_event(self, line):
        """
        Create an Event object from a file line datastring and add it to the
        self.events list.

        Empty lines and lines that start with a #-character are ignored.
        Lines conatining data with an unrecognized syntax are also ignored.

        Each line contains 3 arguments separated with semicolon
        The first and second argument contains a year, a month and a day value
        all separated with commas. The third argument is a text string which
        is the name of the event.
        One row can look like this:
            2008,11,5  ; 2008, 11, 15 ; Foobar bar
        """
        if len(line) == 0:
            return
        elif line.startswith('#'):
            return
        try:
            # A line contains 3 arguments separated with a semicolon
            args = line.split(';');
            if len(args) < 3:
                return
            # The first and second arguments contains the year, month and day
            # values separated with commas
            arg1 = args[0].split(',')
            arg2 = args[1].split(',')
            start_time = dt(eval(arg1[0]),eval(arg1[1]),eval(arg1[2]))
            end_time   = dt(eval(arg2[0]),eval(arg2[1]),eval(arg2[2]))
            event      = Event(start_time,end_time, args[2])
            self.events.append(event)
        except Exception, e:
            logging.fatal('Error', exc_info=e)

    def get_events(self, time_period):
        return [e for e in self.events if e.inside_period(time_period)]

    def preferred_period(self):
        return TimePeriod(dt(2008, 11, 1), dt(2008, 11, 30))
