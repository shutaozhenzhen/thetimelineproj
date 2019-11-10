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

from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.cases.wxapp import WxAppTestCase
from timelinelib.dataimport.timelinexml import import_db_from_timeline_xml, parse_icon
from timelinelib.dataexport.timelinexml import icon_string


class describe_import_timeline_xml(TmpDirTestCase):

    def test_can_import_empty_file(self):
        db = self.import_file_with_content("""
        <timeline>
            <version>0.0.0</version>
            <categories />
            <events />
            <view />
        </timeline>
        """.strip())

    def test_can_import_containers(self):
        db = self.import_file_with_content("""
        <timeline>
            <version>0.0.0</version>
            <categories />
            <events>
                <event>
                    <start>2017-01-01 00:00:00</start>
                    <end>2017-01-01 00:00:00</end>
                    <text>[1]con</text>
                </event>
                <event>
                    <start>2017-01-01 00:00:00</start>
                    <end>2017-01-01 00:00:00</end>
                    <text>(1)sub1</text>
                </event>
            </events>
            <view />
        </timeline>
        """.strip())
        all_events = db.get_all_events()
        containers = [e.text for e in all_events if e.is_container()]
        subevents = [e.text for e in all_events if e.is_subevent()]
        self.assertEqual((containers, subevents), (["con"], ["sub1"]))

    def test_can_import_categories(self):
        db = self.import_file_with_content("""
        <timeline>
            <version>0.0.0</version>
            <categories>
                <category>
                  <name>cat-0</name>
                  <color>50,200,50</color>
                </category>
                <category>
                  <name>cat-1</name>
                  <color>50,200,50</color>
                </category>
                <category>
                  <name>cat-2</name>
                  <color>50,200,50</color>
                </category>
            </categories>
            <events>
                <event>
                    <start>2017-01-01 00:00:00</start>
                    <end>2017-01-01 00:00:00</end>
                    <text>event</text>
                    <category>cat-0</category>
                    <categories>
                        <category>cat-2</category>
                        <category>cat-1</category>
                    </categories>
                </event>
            </events>
            <view />
        </timeline>
        """.strip())
        events = db.get_all_events()
        event = events[0]
        self.assertEqual('cat-0', event.get_category().name)
        self.assertEqual(['cat-2', 'cat-1'], [c.name for c in event.get_categories()])

    def test_duplicate_categories_are_removed(self):
        db = self.import_file_with_content("""
        <timeline>
            <version>0.0.0</version>
            <categories>
                <category>
                  <name>cat-0</name>
                  <color>50,200,50</color>
                </category>
                <category>
                  <name>cat-1</name>
                  <color>50,200,50</color>
                </category>
                <category>
                  <name>cat-2</name>
                  <color>50,200,50</color>
                </category>
            </categories>
            <events>
                <event>
                    <start>2017-01-01 00:00:00</start>
                    <end>2017-01-01 00:00:00</end>
                    <text>event</text>
                    <category>cat-0</category>
                    <categories>
                        <category>cat-0</category>
                        <category>cat-1</category>
                        <category>cat-1</category>
                    </categories>
                </event>
            </events>
            <view />
        </timeline>
        """.strip())
        events = db.get_all_events()
        event = events[0]
        self.assertEqual('cat-0', event.get_category().name)
        self.assertEqual(['cat-1'], [c.name for c in event.get_categories()])

    def test_missing_category_is_taken_from_list(self):
        db = self.import_file_with_content("""
        <timeline>
            <version>0.0.0</version>
            <categories>
                <category>
                  <name>cat-1</name>
                  <color>50,200,50</color>
                </category>
                <category>
                  <name>cat-2</name>
                  <color>50,200,50</color>
                </category>
            </categories>
            <events>
                <event>
                    <start>2017-01-01 00:00:00</start>
                    <end>2017-01-01 00:00:00</end>
                    <text>event</text>
                    <categories>
                        <category>cat-2</category>
                        <category>cat-1</category>
                    </categories>
                </event>
            </events>
            <view />
        </timeline>
        """.strip())
        events = db.get_all_events()
        event = events[0]
        self.assertEqual('cat-2', event.get_category().name)
        self.assertEqual(['cat-1'], [c.name for c in event.get_categories()])

    def import_file_with_content(self, content):
        path = self.get_tmp_path("tmp.timeline")
        with open(path, "w") as f:
            f.write(content)
        return import_db_from_timeline_xml(path)
