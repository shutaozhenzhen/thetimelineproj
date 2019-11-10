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

from timelinelib.canvas.drawing.utils import darken_color
from timelinelib.canvas.drawing.utils import lighten_color
from timelinelib.canvas.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
import timelinelib.meta.overrides as mark


class OtherGradientEventBoxDrawer(DefaultEventBoxDrawer):

    def __init__(self, fuzzy_edges=False):
        self._fuzzy_edges = fuzzy_edges
        self._event = None
        self._rect = None

    @mark.overrides
    def _draw_background(self, dc, rect, event):
        self._event = event
        self._rect = rect
        dc.SetPen(self._get_pen(dc, event))
        if self._fuzzy_edges and event.get_fuzzy():
            self._draw_background_and_fuzzy_edges(dc)
        else:
            self._draw_background_no_fuzzy_edges(dc)

    @mark.overrides
    def _draw_fuzzy_edges(self, dc, rect, event):
        if not self._fuzzy_edges:
            super(OtherGradientEventBoxDrawer, self)._draw_fuzzy_edges(dc, rect, event)

    def _draw_background_no_fuzzy_edges(self, dc):
        dc.DrawRectangle(self._rect)
        inner_rect = wx.Rect(*self._rect)
        inner_rect.Deflate(1, 1)
        dc.GradientFillLinear(inner_rect, self.light_color, self.dark_color, wx.WEST)

    def _draw_background_and_fuzzy_edges(self, dc):
        self._draw_fuzzy_rect_outer_lines(dc)
        self._draw_fuzzy_rect_fill_first_half(dc)
        self._draw_fuzzy_rect_fill_second_half(dc)

    def _draw_fuzzy_rect_outer_lines(self, dc):
        dc.DrawLine(self._rect.GetX(), self._rect.GetY(), self._rect.GetX() + self._rect.GetWidth(), self._rect.GetY())
        dc.DrawLine(self._rect.GetX(), self._rect.GetY() + self._rect.GetHeight() - 1,
                    self._rect.GetX() + self._rect.GetWidth(), self._rect.GetY() + self._rect.GetHeight() - 1)

    def _draw_fuzzy_rect_fill_first_half(self, dc):
        dc.GradientFillLinear(self.half_rect, wx.WHITE, self.dark_color, wx.EAST)

    def _draw_fuzzy_rect_fill_second_half(self, dc):
        rect = self.half_rect
        rect.SetPosition(wx.Point(rect.GetX() + rect.GetWidth(), rect.GetY()))
        dc.GradientFillLinear(rect, wx.WHITE, self.dark_color, wx.WEST)

    @property
    def half_rect(self):
        inner_rect = wx.Rect(*self._rect)
        inner_rect.Deflate(1, 1)
        inner_rect.SetWidth(inner_rect.GetWidth() // 2)
        return inner_rect

    @property
    def light_color(self):
        return lighten_color(self._event.get_color())

    @property
    def dark_color(self):
        return darken_color(self._event.get_color(), factor=0.8)
