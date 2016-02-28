# encoding: utf-8
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


from os.path import abspath

import wx

from timelinelib.config.dotfile import Config
from timelinelib.test.cases.tmpdir import TmpDirTestCase


class describe_config(TmpDirTestCase):

    def test_should_have_default_values_before_config_has_been_read(self):
        self.assertEqual(self.config.get_window_size(), (900, 500))
        self.assertEqual(self.config.get_window_maximized(), False)
        self.assertEqual(self.config.get_show_sidebar(), True)
        self.assertEqual(self.config.get_show_legend(), True)
        self.assertEqual(self.config.get_sidebar_width(), 200)
        self.assertEqual(self.config.get_recently_opened(), [])
        self.assertEqual(self.config.get_open_recent_at_startup(), True)
        self.assertEqual(self.config.get_balloon_on_hover(), True)
        self.assertEqual(self.config.week_start, "monday")
        self.assertEqual(self.config.get_use_inertial_scrolling(), False)
        self.assertEqual(self.config.center_event_texts, False)
        self.assertEqual(self.config.minor_strip_divider_line_colour, (200, 200, 200))

    def test_window_size_can_be_read_after_stored(self):
        self.config.set_window_size((3, 20))
        self.assertEqual(self.config.get_window_size(), (3, 20))

    def test_window_maximized_can_be_read_after_stored(self):
        self.config.set_window_maximized(True)
        self.assertEqual(self.config.get_window_maximized(), True)

    def test_show_sidebar_can_be_read_after_stored(self):
        self.config.set_show_sidebar(False)
        self.assertEqual(self.config.get_show_sidebar(), False)

    def test_show_legend_can_be_read_after_stored(self):
        self.config.set_show_legend(False)
        self.assertEqual(self.config.get_show_legend(), False)

    def test_sidebar_width_can_be_read_after_stored(self):
        self.config.set_sidebar_width(20)
        self.assertEqual(self.config.get_sidebar_width(), 20)

    def test_recently_opened_can_be_read_after_stored(self):
        self.config.append_recently_opened(u"foo")
        self.assertEqual(self.config.get_recently_opened(), [abspath(u"foo")])

    def test_open_recent_at_startup_can_be_read_after_stored(self):
        self.config.set_open_recent_at_startup(False)
        self.assertEqual(self.config.get_open_recent_at_startup(), False)

    def test_balloon_on_hover_can_be_read_after_stored(self):
        self.config.set_balloon_on_hover(False)
        self.assertEqual(self.config.get_balloon_on_hover(), False)

    def test_week_start_can_be_read_after_stored(self):
        self.config.week_start = "sunday"
        self.assertEqual(self.config.week_start, "sunday")

    def test_inertial_scrolling_can_be_read_after_stored(self):
        self.config.use_inertial_scrolling = False
        self.assertEqual(self.config.use_inertial_scrolling, False)

    def test_center_event_texts_can_be_read_after_stored(self):
        self.config.center_event_texts = True
        self.assertEqual(self.config.center_event_texts, True)

    def test_minor_strip_divider_line_colour_can_be_read_after_set(self):
        self.config.minor_strip_divider_line_colour = (100, 0, 0)
        self.assertEqual(self.config.minor_strip_divider_line_colour, (100, 0, 0))

    def test_minor_strip_divider_line_colour_can_be_read_after_stored(self):
        self.config.minor_strip_divider_line_colour = (100, 0, 0)
        self.config.write()
        self.config.read()
        self.assertEqual(self.config.minor_strip_divider_line_colour, (100, 0, 0))

    def test_major_strip_divider_line_colour_can_be_read_after_set(self):
        self.config.major_strip_divider_line_colour = (100, 0, 0)
        self.assertEqual(self.config.major_strip_divider_line_colour, (100, 0, 0))

    def test_major_strip_divider_line_colour_can_be_read_after_stored(self):
        self.config.major_strip_divider_line_colour = (100, 0, 0)
        self.config.write()
        self.config.read()
        self.assertEqual(self.config.major_strip_divider_line_colour, (100, 0, 0))

    def test_config_returns_use_inertial_scrolling_is_true_when_set_to_true(self):
        self.config.set_use_inertial_scrolling(True)
        self.assertTrue(self.config.get_use_inertial_scrolling())

    def test_config_returns_use_inertial_scrolling_is_false_when_set_to_false(self):
        self.config.set_use_inertial_scrolling(False)
        self.assertFalse(self.config.get_use_inertial_scrolling())

    def test_recently_opened_contains_last_5_entries(self):
        self.config.append_recently_opened("1")
        self.config.append_recently_opened("2")
        self.config.append_recently_opened("3")
        self.config.append_recently_opened("4")
        self.config.append_recently_opened("5")
        self.config.append_recently_opened("6")
        self.config.append_recently_opened("7")
        last_five = [abspath(entry) for entry in ["7", "6", "5", "4", "3"]]
        self.assertEqual(self.config.get_recently_opened(), last_five)

    def test_recently_opened_list_does_not_contain_duplicates(self):
        self.config.append_recently_opened("foo")
        self.config.append_recently_opened("bar")
        self.config.append_recently_opened("foo")
        self.assertEqual(
            self.config.get_recently_opened(),
            [abspath("foo"), abspath("bar")])

    def test_converts_recently_opened_path_to_unicode(self):
        self.config.append_recently_opened("non-unicode-path")
        self.assertTrue(isinstance(self.config.get_recently_opened()[0], unicode))

    def test_recently_opened_does_not_store_special_tutorial_file(self):
        self.config.append_recently_opened(":tutorial:")
        self.assertEqual([], self.config.get_recently_opened())

    def test_setting_invalid_week_start_raises_value_error(self):
        def set_invalid_week():
            self.config.week_start = "friday"
        self.assertRaises(ValueError, set_invalid_week)

    def setUp(self):
        TmpDirTestCase.setUp(self)
        self.app = wx.App()
        self.config = Config(self.get_tmp_path("test.config"))

    def tearDown(self):
        TmpDirTestCase.tearDown(self)
