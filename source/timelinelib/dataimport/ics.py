# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.


import random

from datetime import date
from datetime import datetime
from os.path import abspath

from icalendar import Calendar

from timelinelib.calendar.gregorian import Gregorian, GregorianUtils
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.exceptions import TimelineIOError
from timelinelib.canvas.data import Event
from timelinelib.canvas.data import Category
from timelinelib.utils import ex_msg


class IcsLoader(object):

    def load(self, db, path):
        self.events = []
        self.categories = []
        file_contents = self._read_file_content(path)
        cal = self._read_calendar_object(file_contents)
        for vevent in cal.walk("VEVENT"):
            self._load_event(db, vevent)
            self._load_categories(vevent)
        self._save_data_in_db(db)

    def _read_calendar_object(self, file_contents):
        try:
            return Calendar.from_ical(file_contents)
        except Exception, pe:
            msg1 = _("Unable to read calendar data.")
            msg2 = "\n\n" + ex_msg(pe)
            raise TimelineIOError(msg1 + msg2)

    def _read_file_content(self, path):
        ics_file = None
        try:
            ics_file = open(path, "rb")
            return ics_file.read()
        except IOError, e:
            msg = _("Unable to read from file '%s'.")
            whole_msg = (msg + "\n\n%s") % (abspath(path), e)
            raise TimelineIOError(whole_msg)
        finally:
            if ics_file is not None:
                ics_file.close()

    def _save_data_in_db(self, db):
        for event in self.events:
            db.save_event(event)
        for category in self.categories:
            db.save_category(category)

    def _load_event(self, db, vevent):
        start, end = self._extract_start_end(vevent)
        txt = self._get_event_name(vevent)
        event = Event(db.get_time_type(), start, end, txt)
        event.set_data("description", self._get_description(vevent))
        self.events.append(event)

    def _load_categories(self, vevent):
        if "categories" in vevent:
            categories_names = [cat.strip() for cat in vevent["categories"].split(",") if len(cat.strip()) > 0]
            for category_name in categories_names:
                self.categories.append(Category(category_name, self._get_random_color(), None))

    def _get_random_color(self):
        return (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))

    def _get_event_name(self, vevent):
        if "summary" in vevent:
            return vevent["summary"]
        elif "description" in vevent:
            return vevent["description"]
        else:
            return "Unknown"

    def _get_description(self, vevent):
        if "description" in vevent:
            return vevent["description"]
        else:
            return ""

    def _extract_start_end(self, vevent):
        start = self._convert_to_datetime(vevent.decoded("dtstart"))
        if "dtend" in vevent:
            end = self._convert_to_datetime(vevent.decoded("dtend"))
        elif "duration" in vevent:
            end = start + vevent.decoded("duration")
        else:
            end = self._convert_to_datetime(vevent.decoded("dtstart"))
        return (start, end)

    def _convert_to_datetime(self, d):
        if isinstance(d, datetime):
            return Gregorian(d.year, d.month, d.day, d.hour, d.minute, d.second).to_time()
        elif isinstance(d, date):
            return GregorianUtils.from_date(d.year, d.month, d.day).to_time()
        else:
            raise TimelineIOError("Unknown date.")


def import_db_from_ics(path):
    global events
    events = []
    db = MemoryDB()
    db.set_readonly()
    IcsLoader().load(db, path)
    return db
