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
import wx

from timelinelib.plugin.plugins.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
from timelinelib.drawing.utils import darken_color
from timelinelib.drawing.utils import lighten_color
from timelinelib.config.paths import ICONS_DIR


class GradientEventBoxDrawer(DefaultEventBoxDrawer):

    def display_name(self):
        return _("Gradient Event box drawer")

    def run(self, dc, rect, event, selected=False):
        self._draw_background(dc, rect, event)
        self._draw_fuzzy_edges(dc, rect, event)
        self._draw_locked_edges(dc, rect, event)
        self._draw_progress_box(dc, rect, event)
        self._draw_text(dc, rect, event)
        self._draw_contents_indicator(dc, event, rect)
        self._draw_locked_edges(dc, rect, event)
        self._draw_selection_handles(dc, event, rect, selected)
        self._draw_hyperlink(dc, rect, event)

    def _draw_background(self, dc, rect, event):
        dc.SetPen(self._get_border_pen(event))
        dc.DrawRectangleRect(rect)
        inner_rect = wx.Rect(*rect)
        inner_rect.Deflate(1, 1)
        dc.GradientFillLinear(inner_rect, self._get_light_color(event), self._get_dark_color(event), wx.SOUTH)

    def _get_light_color(self, event):
        return lighten_color(self._get_base_color(event))

    def _get_dark_color(self, event):
        return darken_color(self._get_base_color(event), factor=0.8)

    def _draw_locked_start(self, dc, event, rect):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_lock_bitmap(), rect.x - 7, rect.y + 3, True)

    def _draw_locked_end(self, dc, event, rect):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_lock_bitmap(), rect.x + rect.width - 8, rect.y + 3, True)

    def _draw_fuzzy_start(self, dc, rect, event):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_fuzzy_bitmap(), rect.x - 4, rect.y + 4, True)

    def _draw_fuzzy_end(self, dc, rect, event):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_fuzzy_bitmap(), rect.x + rect.width - 8, rect.y + 4, True)

    def _get_lock_bitmap(self):
        return wx.Bitmap(os.path.join(ICONS_DIR, "lock.png"))

    def _get_fuzzy_bitmap(self):
        return wx.Bitmap(os.path.join(ICONS_DIR, "appx.png"))

    def _inflate_clipping_region(self, dc, rect):
        copy = wx.Rect(*rect)
        copy.Inflate(10, 0)
        dc.DestroyClippingRegion()
        dc.SetClippingRect(copy)
