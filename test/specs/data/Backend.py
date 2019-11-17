# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
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


from timelinelib.canvas.data.memorydb.db import MemoryDB
from timelinelib.dataimport.ics import import_db_from_ics
from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.cases.unit import UnitTestCase


class BackendTest(object):

    # These tests should work for any backend. They are tested with different
    # backends below.

    def test_get_all_events_returns_a_list(self):
        all_events = self.backend.get_all_events()
        self.assertTrue(isinstance(all_events, list))

    def test_has_time_type_method(self):
        self.backend.get_time_type()


class MemoryBackendTest(UnitTestCase, BackendTest):

    def setUp(self):
        self.backend = MemoryDB()


class IcsBackendTest(TmpDirTestCase, BackendTest):

    def setUp(self):
        TmpDirTestCase.setUp(self)
        self.backend = import_db_from_ics(self.write_ics_content())

    def test_content(self):
        self.assertEqual(self.backend.get_categories(), [])
        self.assertEqual(len(self.backend.get_all_events()), 1)
        self.assertEqual(self.backend.get_all_events()[0].get_text(),
                         "Bastille Day Party")

    def write_ics_content(self):
        tmp_path = self.get_tmp_path("test.ics")
        f = open(tmp_path, "w")
        f.write(ICS_EXAMPLE)
        f.close()
        return tmp_path


ICS_EXAMPLE = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
BEGIN:VEVENT
UID:uid1@example.com
DTSTAMP:19970714T170000Z
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
DTEND:19970715T035959Z
SUMMARY:Bastille Day Party
END:VEVENT
END:VCALENDAR
"""
