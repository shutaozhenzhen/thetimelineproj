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


class GradientEventBoxDrawer(DefaultEventBoxDrawer):

    @mark.overrides
    def _draw_background(self, dc, rect, event):
        dc.SetPen(self._get_pen(dc, event))
        dc.DrawRectangle(rect)
        light_color = lighten_color(event.get_color())
        dark_color = darken_color(event.get_color(), factor=0.8)
        dc.GradientFillLinear(deflate_rect(rect), light_color, dark_color, wx.SOUTH)


def deflate_rect(rect, dx=1, dy=1):
    return wx.Rect(*rect).Deflate(dx, dy)
