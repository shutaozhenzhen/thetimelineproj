"""
Implementation of a timeline that has a file storage.
"""


import re
import codecs
import os.path
from logging import error as logerror
from logging import info as loginfo

from datetime import datetime

from data import Timeline
from data import TimePeriod
from data import Event
from data import Category


ENCODING = "utf-8"


class ParseException(Exception):
    pass


class FileTimeline2(Timeline):
    """
    Timeline with file storage.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.categories = {} # Maps a name to a Category object
        self.events = []
        self.__load_data()

    def __load_data(self):
        """
        Raise IOError if file can not be opened for reading. This should be
        handled by caller.
        """
        f = None
        if not os.path.exists(self.file_path):
            loginfo("File did not exist '%s'" % self.file_path)
            return
        try:
            f = codecs.open(self.file_path, "r", ENCODING)
            for line in f:
                self.__process_line(line.strip())
        finally:
            if f:
                f.close()

    def __save_data(self):
        """
        Raise IOError if file can not be opened for writing. This should be
        handled by caller.
        """
        f = None
        try:
            f = codecs.open(self.file_path, "w", ENCODING)
            for cat in self.categories.items():
                r, g, b = cat.color
                f.write("CATEGORY:%s;%s,%s,%s\n" % (
                    self.__quote(cat.name), r, g, b))
            for event in self.events:
                f.write("EVENT:%s;%s;%s" % (
                    event.time_period.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    event.time_period.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    self.__quote(event.text)))
                if event.category:
                    f.write(";%s" % self.__quote(event.category.name))
                f.write("\n")
            f.close()
        finally:
            if f:
                f.close()

    def __process_line(self, line):
        loginfo("Processing line '%s'" % line)
        prefixes = (
            ("CATEGORY:", self.__process_category),
            ("EVENT:", self.__process_event),
            ("#", self.__process_comment),
            ("", self.__process_unknown)
        )
        for (prefix, processing_func) in prefixes:
            if line.startswith(prefix):
                processing_func(line[len(prefix):])
                return

    def __split_on_delim(self, text):
        """The delimiter is ; but only of not proceeded by backslash."""
        return re.split(r"(?<!\\);", text)

    def __dequote(self, text):
        return text.replace(r"\;", ";")

    def __quote(self, text):
        return text.replace(r";", "\;")

    def __process_category(self, category_text):
        """Expected format 'name;color'."""
        split = self.__split_on_delim(category_text)
        try:
            if len(split) != 2:
                raise ParseException("Unexpected number of components")
            name = self.__dequote(split[0])
            color = self.__parse_color(split[1])
            self.categories[name] = Category(name, (r, g, b))
        except Exception, e:
            logerror("Unable to parse category (%s): %s" % (e, category_text))

    def __process_event(self, event_text):
        """Expected format 'start_time;end_time;text[;category]'."""
        split = self.__split_on_delim(event_text)
        try:
            if len(split) != 3 and len(split) != 4:
                raise ParseException("Unexpected number of components")
            start_time = self.__parse_time(split[0])
            end_time = self.__parse_time(split[1])
            text = self.__dequote(split[2])
            category_text = None
            if len(split) == 4:
                category_text = self.__dequote(split[3])
            category = self.categories.get(category_text, None)
            self.events.append(Event(start_time, end_time, text, category))
        except Exception, e:
            logerror("Unable to parse event (%s): %s" % (e, event_text))

    def __process_comment(self, comment):
        pass

    def __process_unknown(self, line):
        # Ignore empty lines
        if line:
            logerror("Skipping unknown line: '%s'" % line)

    def __parse_color(self, color_string):
        """
        Return a tuple (r, g, b) or raise exception.
        
        Expected format 'r,g,b'.
        """
        def verify_255_number(num):
            if num < 0 or num > 255:
                raise ParseException("Color number not in range [0, 255]")
        match = re.search(r"^(\d+),(\d+),(\d+)$", color_string)
        if match:
            r, g, b = int(match(1)), int(match(2)), int(match(3))
            verify_255_number(r)
            verify_255_number(g)
            verify_255_number(b)
            return (r, g, b)
        else:
            raise ParseException("Color not on correct format")

    def __parse_time(self, time_str):
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

    def get_events(self, time_period):
        return [e for e in self.events if e.inside_period(time_period)]

    def preferred_period(self):
        return TimePeriod(datetime(2008, 11, 1), datetime(2008, 11, 30))

    def new_event(self, event):
        self.events.append(event)
        self.__save_data()

    def delete_selected_events(self):
        self.events = [e for e in self.events if not e.selected]
        self.__save_data()

    def reset_selection(self):
        for e in self.events:
            e.selected = False
