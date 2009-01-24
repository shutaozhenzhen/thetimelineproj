"""
Implementation of timeline with file storage.

The class `FileTimeline` implements the timeline interface.
"""


import re
import codecs
import os.path
from logging import error as logerror
from logging import info as loginfo
from datetime import datetime
from datetime import timedelta

from data import Timeline
from data import TimePeriod
from data import Event
from data import Category
from data import time_period_center
from version import get_version
from gui import display_error_message


ENCODING = "utf-8"


class ParseException(Exception):
    pass


class FileTimeline(Timeline):
    """
    Implements the timeline interface.

    The comments in `Timeline` describes what the public methods should do.
    """

    def __init__(self, file_path):
        """Create a new timeline and read data from file."""
        self.file_path = file_path
        self.__load_data()

    def __load_data(self):
        self.preferred_period = None
        self.categories = []
        self.events = []
        self.disable_save_due_to_corrupt_data = False
        if not os.path.exists(self.file_path): 
            # Nothing to load if file does not exist
            return
        loginfo("Opening file '%s'" % self.file_path)
        f = None
        try:
            try:
                f = codecs.open(self.file_path, "r", ENCODING)
            except IOError, e:
                display_error_message("Unable to read data from timeline.\n\n%s" % e)
            else:
                data_corrupt = False
                for line in f:
                    if not self.__process_line(line.strip()):
                        data_corrupt = True
                if data_corrupt:
                    display_error_message("Timeline data corrupt. Enable logging and open the timeline again to get more information about the problem.")
                    self.disable_save_due_to_corrupt_data = True
        finally:
            if f:
                f.close()

    def __save_data(self):
        if self.disable_save_due_to_corrupt_data:
            display_error_message("Save disabled because timeline data was corrupt.")
            return
        f = None
        try:
            try:
                f = codecs.open(self.file_path, "w", ENCODING)
            except IOError, e:
                display_error_message("Unable to save timeline data.\n\n%s" % e)
            else:
                f.write("# Written by Timeline %s on %s\n" % (
                        get_version(),
                        time_str(datetime.now())))
                if self.preferred_period:
                    f.write("PREFERRED-PERIOD:%s;%s\n" % (
                        time_str(self.preferred_period.start_time),
                        time_str(self.preferred_period.end_time)))
                for cat in self.categories:
                    r, g, b = cat.color
                    f.write("CATEGORY:%s;%s,%s,%s\n" % (quote(cat.name),
                                                        r, g, b))
                for event in self.events:
                    f.write("EVENT:%s;%s;%s" % (
                        time_str(event.time_period.start_time),
                        time_str(event.time_period.end_time),
                        quote(event.text)))
                    if event.category:
                        f.write(";%s" % quote(event.category.name))
                    f.write("\n")
        finally:
            if f:
                f.close()

    def __process_line(self, line):
        """Process data on `line` and return True if successful."""
        loginfo("Processing line '%s'" % line)
        # Map prefixes to functions that handle the rest of that line
        prefixes = (
            ("PREFERRED-PERIOD:", self.__process_preferred_period),
            ("CATEGORY:", self.__process_category),
            ("EVENT:", self.__process_event),
            ("#", self.__process_comment),
            # Catch all (make sure this function always return something)
            ("", self.__process_unknown),
        )
        for (prefix, processing_func) in prefixes:
            if line.startswith(prefix):
                return processing_func(line[len(prefix):])

    def __process_preferred_period(self, period_text):
        """Expected format 'start_time;end_time'."""
        split = split_on_delim(period_text)
        try:
            if len(split) != 2:
                raise ParseException("Unexpected number of components")
            self.preferred_period = TimePeriod(parse_time(split[0]),
                                               parse_time(split[1]))
            return True
        except ParseException, e:
            logerror("Unable to parse preferred period from '%s'" % (
                     period_text), exc_info=e)
            return False

    def __process_category(self, category_text):
        """Expected format 'name;color'."""
        split = split_on_delim(category_text)
        try:
            if len(split) != 2:
                raise ParseException("Unexpected number of components")
            name = dequote(split[0])
            color = parse_color(split[1])
            self.categories.append(Category(name, color))
            return True
        except ParseException, e:
            logerror("Unable to parse category from '%s'" % category_text,
                     exc_info=e)
            return False

    def __process_event(self, event_text):
        """Expected format 'start_time;end_time;text[;category]'."""
        split = split_on_delim(event_text)
        try:
            if len(split) != 3 and len(split) != 4:
                raise ParseException("Unexpected number of components")
            start_time = parse_time(split[0])
            end_time = parse_time(split[1])
            text = dequote(split[2])
            cat_name = None
            if len(split) == 4:
                cat_name = dequote(split[3])
            category = self.__get_category(cat_name)
            self.events.append(Event(start_time, end_time, text, category))
            return True
        except ParseException, e:
            logerror("Unable to parse event from '%s'" % event_text,
                     exc_info=e)
            return False

    def __process_comment(self, comment):
        return True

    def __process_unknown(self, line):
        if line.strip():
            logerror("Skipping unknown line: '%s'" % line)
            # An unknown line can not be processed successfully
            return False
        # Ignore empty lines
        return True

    def __get_category(self, name):
        for cat in self.categories:
            if cat.name == name:
                return cat
        return None

    def get_events(self, time_period):
        return [e for e in self.events if e.inside_period(time_period)]

    def add_event(self, event):
        self.events.append(event)
        self.__save_data()

    def event_edited(self, event):
        self.__save_data()

    def delete_selected_events(self):
        self.events = [e for e in self.events if not e.selected]
        self.__save_data()

    def get_categories(self):
        # Make sure the original list can't be modified
        return tuple(self.categories)

    def add_category(self, category):
        self.categories.append(category)
        self.__save_data()

    def category_edited(self, category):
        self.__save_data()

    def delete_category(self, category):
        if category in self.categories:
            self.categories.remove(category)
        for event in self.events:
            if event.category == category:
                event.category = None
        self.__save_data()

    def get_preferred_period(self):
        if self.preferred_period:
            return self.preferred_period
        return time_period_center(datetime.now(), timedelta(days=30))

    def set_preferred_period(self, period):
        self.preferred_period = period
        self.__save_data()

    def reset_selection(self):
        for e in self.events:
            e.selected = False


def parse_color(color_string):
    """
    Return a tuple (r, g, b) or raise exception.
    
    Expected format 'r,g,b'.
    """
    def verify_255_number(num):
        if num < 0 or num > 255:
            raise ParseException("Color number not in range [0, 255]")
    match = re.search(r"^(\d+),(\d+),(\d+)$", color_string)
    if match:
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        verify_255_number(r)
        verify_255_number(g)
        verify_255_number(b)
        return (r, g, b)
    else:
        raise ParseException("Color not on correct format")


def parse_time(time_str):
    """
    Return a DateTime or raise exception.

    Expected format 'year-month-day hour:minute:second'.
    """
    match = re.search(r"^(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)$", time_str)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))
        try:
            return datetime(year, month, day, hour, minute, second)
        except ValueError:
            raise ParseException("Invalid time")
    else:
        raise ParseException("Time not on correct format")


def time_str(time):
    """
    Return time formatted for writing to file.
    """
    return "%s-%s-%s %s:%s:%s" % (time.year, time.month, time.day,
                                  time.hour, time.minute, time.second)


def split_on_delim(text):
    """
    The delimiter is ; but only of not proceeded by backslash.

    Examples:

        'foo;bar' -> ['foo', 'bar']
        'foo\;bar;barfoo -> ['foo\;bar', 'barfoo']
    """
    return re.split(r"(?<!\\);", text)


def dequote(text):
    return text.replace(r"\;", ";")


def quote(text):
    return text.replace(";", r"\;")
