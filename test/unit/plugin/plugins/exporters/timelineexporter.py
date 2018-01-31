# -*- coding: utf-8 -*-
#
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


import os

from mock import Mock

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.plugin.plugins.exporters.timelineexporter import CsvExporter
from timelinelib.plugin.plugins.exporters.timelineexporter import TimelineExporter
from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import an_event_with


CSV_FILE = "test.csv"


class TimelineExporterTestCase(TmpDirTestCase):

    def setUp(self):
        TmpDirTestCase.setUp(self)
        db = MemoryDB()
        db.save_event(an_event_with(text="foo\nbar", time="11 Jul 2014 10:11"))
        db.save_category(a_category_with("Cat\"1\""))
        self.plugin = TimelineExporter()
        self.plugin.timeline = db

    def simulate_dialog_entries(self, export_events, event_fields, export_categories, category_fields):
        self.dlg = Mock()
        self.dlg.GetExportEvents.return_value = export_events
        self.dlg.GetExportCategories.return_value = export_categories
        self.dlg.GetEventFields.return_value = event_fields
        self.dlg.GetCategoryFields.return_value = category_fields
        self.dlg.GetTextEncoding.return_value = "utf-8"
        self.dlg.GetTextEncodingErrorStrategy.return_value = "strict"


class describe_timeline_exporter(TimelineExporterTestCase):

    def test_is_a_plugin(self):
        self.assertTrue(self.plugin.isplugin())

    def test_event_csv_data_saved_in_file(self):
        self.simulate_dialog_entries(True, [_("Text"), _("Start")], False, [])
        CsvExporter(
            self.plugin.timeline,
            self.get_tmp_path(CSV_FILE),
            self.dlg
        ).export()
        self.assertEqual(
            self.read(CSV_FILE),
            (u"\"⟪Events⟫\";\n\"%s\";\"%s\";\n\"foo\nbar\";2014-07-11 10:11:00;\n\n" % (_("Text"), _("Start"))).encode("utf-8")
        )

    def test_category_csv_data_saved_in_file(self):
        self.simulate_dialog_entries(False, [], True, [_("Name"), _("Color")])
        CsvExporter(
            self.plugin.timeline,
            self.get_tmp_path(CSV_FILE),
            self.dlg
        ).export()
        self.assertEqual(
            self.read(CSV_FILE),
            (u"\"⟪Categories⟫\";\n\"%s\";\"%s\";\n\"Cat\"\"1\"\"\";(255, 0, 0);\n" % (_("Name"), _("Color"))).encode("utf-8")
        )
