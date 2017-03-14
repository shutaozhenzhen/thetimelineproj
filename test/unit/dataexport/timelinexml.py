# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


from timelinelib.canvas.data.db import MemoryDB
from timelinelib.dataexport.timelinexml import export_db_to_timeline_xml
from timelinelib.dataimport.timelinexml import import_db_from_timeline_xml
from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.utils import an_event_with


class describe_export_db_to_timeline_xml(TmpDirTestCase):

    def test_can_export_events_with_empty_text(self):
        self.empty_db.save_event(an_event_with(text=""))
        export_db_to_timeline_xml(self.empty_db, self.export_path)
        db = import_db_from_timeline_xml(self.export_path)
        self.assertEqual(len(db.get_all_events()), 1)
        self.assertEqual(db.get_all_events()[0].get_default_color(), (200, 200, 200))

    def test_can_export_events_with_default_color(self):
        self.empty_db.save_event(an_event_with(default_color=(100, 100, 100)))
        export_db_to_timeline_xml(self.empty_db, self.export_path)
        db = import_db_from_timeline_xml(self.export_path)
        self.assertEqual(len(db.get_all_events()), 1)
        self.assertEqual(db.get_all_events()[0].get_default_color(), (100, 100, 100))

    def setUp(self):
        TmpDirTestCase.setUp(self)
        self.export_path = self.get_tmp_path("export.timeline")
        self.empty_db = MemoryDB()
