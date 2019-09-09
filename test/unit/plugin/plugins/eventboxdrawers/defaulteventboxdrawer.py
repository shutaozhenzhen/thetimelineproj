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


from timelinelib.plugin.factory import EVENTBOX_DRAWER
from timelinelib.plugin.plugins.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import an_event_with


class describe_default_event_box_drawer(UnitTestCase):

    def test_is_a_plugin(self):
        self.assertTrue(self.plugin.isplugin())

    def test_is_an_event_box_drawer(self):
        self.assertEqual(EVENTBOX_DRAWER, self.plugin.service())

    def test_has_a_display_name(self):
        self.assertTrue(len(self.plugin.display_name()) > 0)

    def test_base_color_is_gray_when_event_has_no_category(self):
        event = an_event_with(category=None)
        self.assertEqual((200, 200, 200), self.plugin.run()._get_event_color(event))

    def test_base_color_is_category_color_when_event_has_category(self):
        category = a_category_with(name="test", color=(100, 100, 100))
        event = an_event_with(category=category)
        self.assertEqual((100, 100, 100), self.plugin.run()._get_event_color(event))

    def test_border_color_is_dark_gray_when_event_has_no_category(self):
        event = an_event_with(category=None)
        self.assertEqual((140, 140, 140), self.plugin.run()._get_border_color(event))

    def test_base_color_is_dark_category_color_when_event_has_category(self):
        category = a_category_with(name="test", color=(100, 100, 100))
        event = an_event_with(category=category)
        self.assertEqual((70, 70, 70), self.plugin.run()._get_border_color(event))

    def setUp(self):
        self.plugin = DefaultEventBoxDrawer()
