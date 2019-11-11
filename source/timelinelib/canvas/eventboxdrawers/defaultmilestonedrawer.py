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

from timelinelib.canvas.drawing.utils import black_solid_pen
from timelinelib.canvas.drawing.utils import black_solid_brush


class DefaultMilestoneDrawer:

    HANDLE_SIZE = 6
    HALF_HANDLE_SIZE = 3

    def __init__(self, rect, event, selected):
        self._rect = rect
        self._event = event
        self._selected = selected

    def draw(self, dc):
        dc.DestroyClippingRegion()
        self._draw_rectangle(dc)
        self.draw_label(dc)
        if self._selected:
            self.draw_move_handle(dc)

    def _draw_rectangle(self, dc):
        dc.SetPen(black_solid_pen(1))
        dc.SetBrush(wx.Brush(wx.Colour(*self._event.get_color()), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(self._rect)

    def draw_label(self, dc):
        label = self._event.text[0] if self._event.text else " "
        draw_centered_text(dc, self._rect, label)

    def draw_move_handle(self, dc):
        dc.SetBrush(black_solid_brush())
        point = center_point_with_offset(self._rect, self.HALF_HANDLE_SIZE, self.HALF_HANDLE_SIZE)
        size = wx.Size(self.HANDLE_SIZE, self.HANDLE_SIZE)
        dc.DrawRectangle(wx.Rect(point, size))


def draw_centered_text(dc, rect, label):
    size = dc.GetTextExtent(label)
    point = center_point_with_offset(rect, size.width // 2, size.height // 2)
    dc.DrawText(label, point)


def center_point_with_offset(rect, dx=0, dy=0):
    y = rect.Y + rect.Height // 2 - dy
    x = rect.X + rect.Width // 2 - dx
    return wx.Point(x, y)
