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

import wx

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.dataexport.timelinexml import export_db_to_timeline_xml, icon_string
from timelinelib.dataimport.timelinexml import import_db_from_timeline_xml, parse_icon
from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.cases.wxapp import WxAppTestCase
from timelinelib.test.utils import a_container
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import a_category_with


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

    def test_can_export_containers(self):
        self.empty_db.save_events(
            a_container(name="con", category=None, sub_events=[
                ("sub1", None),
            ])
        )
        content = self.export_and_read()
        self.assertIn("[1]con", content)
        self.assertIn("(1)sub1", content)

    def test_can_export_categories(self):
        cat1 = a_category_with(name='cat1')
        cat2 = a_category_with(name='cat2')
        cat3 = a_category_with(name='cat3')
        self.empty_db.save_category(cat1)
        self.empty_db.save_category(cat2)
        self.empty_db.save_category(cat3)
        self.empty_db.save_event(
            an_event_with(category=cat1, categories=[cat3, cat2])
        )
        content = self.export_and_read()
        expected = """\
      <category>cat1</category>
      <categories>
        <category>cat3</category>
        <category>cat2</category>
      </categories>"""
        self.assertIn(expected, content)

    def test_can_export_categories_and_set_missing_category(self):
        cat1 = a_category_with(name='cat1')
        cat2 = a_category_with(name='cat2')
        cat3 = a_category_with(name='cat3')
        self.empty_db.save_category(cat1)
        self.empty_db.save_category(cat2)
        self.empty_db.save_category(cat3)
        self.empty_db.save_event(
            an_event_with(category=None, categories=[cat1, cat3, cat2])
        )
        content = self.export_and_read()
        expected = """\
      <category>cat1</category>
      <categories>
        <category>cat3</category>
        <category>cat2</category>
      </categories>"""
        self.assertIn(expected, content)

    def test_removing_category_takes_next_from_list(self):
        cat1 = a_category_with(name='cat1')
        cat2 = a_category_with(name='cat2')
        cat3 = a_category_with(name='cat3')
        self.empty_db.save_category(cat1)
        self.empty_db.save_category(cat2)
        self.empty_db.save_category(cat3)
        evt = an_event_with(category=None, categories=[cat1, cat3, cat2])
        self.empty_db.save_event(evt)
        evt.category = None
        self.empty_db.save_event(evt)
        content = self.export_and_read()
        expected = """\
      <category>cat3</category>
      <categories>
        <category>cat2</category>
      </categories>"""
        self.assertIn(expected, content)

    def export_and_read(self):
        export_db_to_timeline_xml(self.empty_db, self.export_path)
        return self.read("export.timeline")

    def setUp(self):
        TmpDirTestCase.setUp(self)
        self.export_path = self.get_tmp_path("export.timeline")
        self.empty_db = MemoryDB()


class IconTestCase(WxAppTestCase):

    IMAGE_PATH1 = f'..{os.sep}icons{os.sep}16.png'
    IMAGE_PATH2 = f'icons{os.sep}16.png'

    def test_bitmap_can_be_converted_to_string_and_back(self):
        if os.path.exists(self.IMAGE_PATH1):
            self.assertTrue(parse_icon(self.create_a_bitmap_string(self.IMAGE_PATH1)).IsOk())
        elif os.path.exists(self.IMAGE_PATH2):
            self.assertTrue(parse_icon(self.create_a_bitmap_string(self.IMAGE_PATH2)).IsOk())
        else:
            print(f'Image not found: {self.IMAGE_PATH1} or: {self.IMAGE_PATH2}')

    def create_a_bitmap_string(self, path):
        image = wx.Image(0, 0)
        image.LoadFile(path)
        self.bitmap = image.ConvertToBitmap()
        return icon_string(self.bitmap)
