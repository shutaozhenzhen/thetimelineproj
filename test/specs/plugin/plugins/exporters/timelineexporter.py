# Copyright (C) 2009, 2010, 2011  Rickard Lindberg, Roger Lindberg
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

import unittest
from mock import Mock

from timelinelib.plugin.plugins.exporters.timelineexporter import TimelineExporter
from timelinelib.plugin.plugins.exporters.timelineexporter import CsvExporter
from timelinelib.data.db import MemoryDB
from specs.utils import an_event_with
from specs.utils import a_category_with


CSV_FILE = "test.csv"


class TimelineExporterTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin = TimelineExporter()
        self.plugin.text_encoding = "cp1250"
        self.plugin.timeline = MemoryDB()
        self.plugin.timeline._events._events.append(an_event_with(text="foo", time="11 Jul 2014 10:11"))
        self.plugin.timeline._events._categories.append(a_category_with("Cat1"))
        self.open_tempfile_for_writing()

    def tearDown(self):
        self.close_tempfile()
        os.remove(CSV_FILE)
        unittest.TestCase.tearDown(self)

    def open_tempfile_for_writing(self):
        self.tempfile = open(CSV_FILE, "w")

    def open_tempfile_for_reading(self):
        self.tempfile = open(CSV_FILE, "r")

    def close_tempfile(self):
        self.tempfile.close()

    def get_tempfile_content(self):
        self.close_tempfile()
        self.open_tempfile_for_reading()
        content = self.tempfile.read()
        self.close_tempfile()
        return content

    def simulate_dialog_entries(self, export_events, event_fields, export_categories, category_fields):
        self.dlg = Mock()
        self.dlg.get_export_events.return_value = export_events
        self.dlg.get_export_categories.return_value = export_categories
        self.dlg.get_event_fields.return_value = event_fields
        self.dlg.get_category_fields.return_value = category_fields
        self.dlg.get_text_encoding.return_value = "cp1252"


class describe_timeline_exporter(TimelineExporterTestCase):

    def test_is_a_plugin(self):
        self.assertTrue(self.plugin.isplugin())

    def test_event_csv_data_saved_in_file(self):
        self.open_tempfile_for_writing()
        self.simulate_dialog_entries(True, ["Text", "Start"], False, [])
        CsvExporter(self.plugin.timeline, CSV_FILE, self.dlg).export()
        content = self.get_tempfile_content()
        self.assertEqual("#Events#\nText;Start;\nfoo;2014-07-11 10:11:00;\n\n", content)

    def test_category_csv_data_saved_in_file(self):
        self.open_tempfile_for_writing()
        self.simulate_dialog_entries(False, [], True, ["Name", "Color"])
        CsvExporter(self.plugin.timeline, CSV_FILE, self.dlg).export()
        content = self.get_tempfile_content()
        self.assertEqual("#Categories#\nName;Color;\nCat1;(255, 0, 0);\n", content)
