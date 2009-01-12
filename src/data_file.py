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

    _data_source = None

    def __init__(self, data_source):
        """Load events from data in the given file, data_source."""
        logging.debug('FileTimeline creation')
        self._data_source = data_source
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
            2008-11-5  ; 2008-11-15 ; Foobar bar
        or
            2008-11-5-10:12:37  ; 2008-11-15-11:23:42 ; Foobar bar
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
            arg1 = args[0].split('-')
            arg2 = args[1].split('-')

            if len(arg1) > 3:
                arg11 = arg1[3].split(':')
                if (len(arg11) > 2):
                    start_time = dt(int(arg1[0]),int(arg1[1]),int(arg1[2]),
                                    int(arg11[0]),int(arg11[1]),int(arg11[2]))
                else:
                    start_time = dt(int(arg1[0]),int(arg1[1]),int(arg1[2]))
            else:
                start_time = dt(int(arg1[0]),int(arg1[1]),int(arg1[2]))

            if len(arg2) > 3:
                arg22 = arg2[3].split(':')
                if (len(arg22) > 2):
                    end_time   = dt(int(arg2[0]),int(arg2[1]),int(arg2[2]),int(arg22[0]),int(arg22[1]),int(arg22[2]))
                else:
                    end_time   = dt(int(arg2[0]),int(arg2[1]),int(arg2[2]))
            else:
                end_time   = dt(int(arg2[0]),int(arg2[1]),int(arg2[2]))

            event      = Event(start_time,end_time, args[2])
            self.events.append(event)
        except Exception, e:
            logging.fatal('Error', exc_info=e)

    def get_events(self, time_period):
        return [e for e in self.events if e.inside_period(time_period)]

    def reset_selection(self):
        for e in self.events:
            e.selected = False

    def get_preferred_period(self):
        return TimePeriod(dt(2008, 11, 1), dt(2008, 11, 30))

    def add_event(self, event):
        """Add a new event to the Timeline"""
        logging.debug("add_event called")
        self.events.append(event)
        self.save_events()

    def delete_selected_events(self):
        """Delete all selected events"""
        self.events = [e for e in self.events if not e.selected]
        self.save_events()

    def save_events(self):
        """Save all events to file"""
        logging.debug("save_events called")
        f = open(self._data_source, 'w')
        try:
            try:
                for event in self.events:
                    line = "%s-%s-%s-%s:%s:%s;%s-%s-%s-%s:%s:%s;%s\n" % (event.time_period.start_time.year,
                           event.time_period.start_time.month,
                           event.time_period.start_time.day,
                           event.time_period.start_time.hour,
                           event.time_period.start_time.minute,
                           event.time_period.start_time.second,
                           event.time_period.end_time.year,
                           event.time_period.end_time.month,
                           event.time_period.end_time.day,
                           event.time_period.end_time.hour,
                           event.time_period.end_time.minute,
                           event.time_period.end_time.second,
                           event.text)
                    f.writelines(line)
            except Exception, e:
                logging.fatal('Error when adding record to file ' + self._data_source,
                              exc_info=e)
        finally:
            f.close()
