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


import wx
from unittest.mock import Mock

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.canvas.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
from timelinelib.canvas.eventboxdrawers.defaulteventboxdrawer import INNER_PADDING


DEFAULT_TEXT = "test"


class describe_default_exventbox_drawer_draw_text(UnitTestCase):

    def test_when_rect_has_zero_width_text_is_not_drawn(self):
        rect = wx.Rect(0, 0, 0, 0)
        self.drawer._draw_text(self.dc, rect, self.event)
        self.assertEqual(self.dc.DrawText.call_count, 0)

    def test_when_rect_has_inner_padding_width_text_is_not_drawn(self):
        rect = wx.Rect(0, 0, INNER_PADDING * 2, 0)
        self.drawer._draw_text(self.dc, rect, self.event)
        self.assertEqual(self.dc.DrawText.call_count, 0)

    def test_non_centered_text_is_left_aligned(self):
        WIDTH = 100
        HEIGHT = 20
        rect = wx.Rect(0, 0, WIDTH, HEIGHT)
        self.drawer.center_text = False
        self.drawer._draw_text(self.dc, rect, self.event)
        self.dc.SetClippingRegion.assert_called_with(wx.Rect(INNER_PADDING, INNER_PADDING, WIDTH - 2 * INNER_PADDING, HEIGHT - 2 * INNER_PADDING))
        self.dc.DrawText.assert_called_with(DEFAULT_TEXT, INNER_PADDING, INNER_PADDING)

    def test_centered_text_is_not_left_aligned(self):
        WIDTH = 100
        HEIGHT = 20
        rect = wx.Rect(0, 0, WIDTH, HEIGHT)
        self.drawer.center_text = True
        self.drawer._draw_text(self.dc, rect, self.event)
        self.dc.SetClippingRegion.assert_called_with(wx.Rect(INNER_PADDING, INNER_PADDING, WIDTH - 2 * INNER_PADDING, HEIGHT - 2 * INNER_PADDING))
        self.dc.DrawText.assert_called_with(DEFAULT_TEXT, (WIDTH - 2 * INNER_PADDING - 50) / 2 + INNER_PADDING, INNER_PADDING)

    def test_centered_text_is_left_aligned_if_text_is_too_long_to_fit(self):
        WIDTH = 100
        HEIGHT = 20
        rect = wx.Rect(0, 0, WIDTH, HEIGHT)
        self.dc.GetTextExtent.return_value = (500, 0)
        self.drawer.center_text = True
        self.drawer._draw_text(self.dc, rect, self.event)
        self.dc.SetClippingRegion.assert_called_with(wx.Rect(INNER_PADDING, INNER_PADDING, WIDTH - 2 * INNER_PADDING, HEIGHT - 2 * INNER_PADDING))
        self.dc.DrawText.assert_called_with(DEFAULT_TEXT, INNER_PADDING, INNER_PADDING)

    def test_non_centered_text_is_left_ajusted_when_fuzzy(self):
        WIDTH = 100
        HEIGHT = 20
        self.event.get_fuzzy.return_value = True
        rect = wx.Rect(0, 0, WIDTH, HEIGHT)
        self.drawer.center_text = False
        self.drawer._draw_text(self.dc, rect, self.event)
        self.dc.SetClippingRegion.assert_called_with(wx.Rect(INNER_PADDING, INNER_PADDING, WIDTH - 2 * INNER_PADDING, HEIGHT - 2 * INNER_PADDING))
        self.dc.DrawText.assert_called_with(DEFAULT_TEXT, INNER_PADDING + HEIGHT / 2, INNER_PADDING)

    def test_non_centered_text_is_left_ajusted_when_locked(self):
        WIDTH = 100
        HEIGHT = 20
        self.event.get_locked.return_value = True
        rect = wx.Rect(0, 0, WIDTH, HEIGHT)
        self.drawer.center_text = False
        self.drawer._draw_text(self.dc, rect, self.event)
        self.dc.SetClippingRegion.assert_called_with(wx.Rect(INNER_PADDING, INNER_PADDING, WIDTH - 2 * INNER_PADDING, HEIGHT - 2 * INNER_PADDING))
        self.dc.DrawText.assert_called_with(DEFAULT_TEXT, INNER_PADDING + HEIGHT / 2, INNER_PADDING)

    def test_if_checkmark_is_to_be_used_it_is_placed_as_first_char_in_text(self):
        WIDTH = 100
        HEIGHT = 20
        self.event.get_locked.return_value = True
        self.event.get_progress.return_value = 100
        rect = wx.Rect(0, 0, WIDTH, HEIGHT)
        self.drawer.center_text = False
        self.drawer.view_properties.get_display_checkmark_on_events_done.return_value = True
        self.drawer._draw_text(self.dc, rect, self.event)
        self.dc.SetClippingRegion.assert_called_with(wx.Rect(INNER_PADDING, INNER_PADDING, WIDTH - 2 * INNER_PADDING, HEIGHT - 2 * INNER_PADDING))
        self.dc.DrawText.assert_called_with(u"\u2714" + DEFAULT_TEXT, INNER_PADDING + HEIGHT / 2, INNER_PADDING)

    def test_milestone_with_no_text_can_be_drawn(self):
        with self.wxapp():
            self.event.get_text.return_value = ""
            self.event.get_default_color.return_value = (127, 127, 127)
            self.event.get_category.return_value = None
            rect = wx.Rect(0, 0, 100, 20)
            scene = Mock()
            try:
                self.drawer._draw_milestone_event(self.dc, rect, scene, self.event, False)
                self.dc.DrawText.assert_called_with(" ", 6, 2)
            except IndexError:
                self.fail("Exception was not expected")

    def setUp(self):
        self.drawer = DefaultEventBoxDrawer()
        self.drawer.view_properties = Mock()
        self.dc = Mock()
        self.dc.GetTextExtent.return_value = (50, 0)
        self.event = Mock()
        self.event.is_container.return_value = False
        self.event.get_fuzzy.return_value = False
        self.event.get_locked.return_value = False
        self.event.get_text.return_value = DEFAULT_TEXT
