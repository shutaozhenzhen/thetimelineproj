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


import os

from timelinelib.dataimport.ics import import_db_from_ics
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.canvas.data.exceptions import TimelineIOError
from timelinelib.time.timeline import TimeDelta


ICS_CONTENT = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN

BEGIN:VEVENT
CATEGORIES:MEETING 1, MEETING 2
UID:uid1@example.com
DTSTAMP:19970714T170000Z
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
DTEND:19970715T035959Z
SUMMARY:Bastille Day Party
DESCRIPTION:Steve and John to review newest proposal material
END:VEVENT

END:VCALENDAR
"""

ICS_CONTENT_WITHOUT_DTEND = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN

BEGIN:VEVENT
CATEGORIES:MEETING 1, MEETING 2
UID:uid1@example.com
DTSTAMP:19970714T170000Z
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
SUMMARY:Bastille Day Party
DESCRIPTION:Steve and John to review newest proposal material
END:VEVENT

END:VCALENDAR
"""

ICS_CONTENT_WITH_DURATION = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN

BEGIN:VEVENT
CATEGORIES:MEETING 1, MEETING 2
UID:uid1@example.com
DTSTAMP:19970714T170000Z
DURATION:PT1H
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
SUMMARY:Bastille Day Party
DESCRIPTION:Steve and John to review newest proposal material
END:VEVENT

END:VCALENDAR
"""

INVALID_ICS_CONTENT = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN

BEGIN:VEVENT
CATEGORIES:MEETING1
UID:uid1@example.com
DTSTAMP:19970714T170000Z
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
DTEND:19970715T035959Z
SUMMARY:Bastille Day Party


END:VCA
"""


class describe_import_ics(UnitTestCase):

    def test_can_import_events_from_ics_file(self):
        self.given_ics_file(ICS_CONTENT)
        db = self.when_ics_file_imported()
        event_names = [event.get_text() for event in db.get_all_events()]
        self.assertEqual(len(event_names), 1)
        self.assertEqual(event_names[0], "Bastille Day Party")

    def test_can_import_events_from_ics_file_with_no_dtend(self):
        self.given_ics_file(ICS_CONTENT_WITHOUT_DTEND)
        db = self.when_ics_file_imported()
        event = db.get_all_events()[0]
        self.assertEqual(event.time_period.start_time, event.time_period.end_time)

    def test_can_import_events_from_ics_file_with_duration(self):
        self.given_ics_file(ICS_CONTENT_WITH_DURATION)
        db = self.when_ics_file_imported()
        event = db.get_all_events()[0]
        self.assertEqual(event.time_period.end_time, event.time_period.start_time + TimeDelta(60 * 60))

    def test_can_import_categories_from_ics_file(self):
        self.given_ics_file(ICS_CONTENT)
        db = import_db_from_ics(self.ics_file_path)
        category_names = [category.get_name() for category in db.get_categories()]
        self.assertEqual(len(category_names), 2)
        self.assertEqual(category_names[0], "MEETING 1")
        self.assertEqual(category_names[1], "MEETING 2")

    def test_invalid_file_raises_exception(self):
        self.assertRaises(TimelineIOError, import_db_from_ics, "...")

    def test_invalid_file_content_raises_exception(self):
        self.given_ics_file(INVALID_ICS_CONTENT)
        self.assertRaises(TimelineIOError, import_db_from_ics, self.ics_file_path)

    def given_ics_file(self, name):
        self.ics_file_path = "ics_file.txt"
        with open(self.ics_file_path, "w") as f:
            f.write(name)

    def when_ics_file_imported(self):
        return import_db_from_ics(self.ics_file_path)

    def setUp(self):
        self.ics_file_path = "ics_file.txt"

    def tearDown(self):
        try:
            os.remove(self.ics_file_path)
        except:
            pass