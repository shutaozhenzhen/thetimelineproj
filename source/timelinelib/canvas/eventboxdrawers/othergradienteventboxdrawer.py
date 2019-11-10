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
    """
    This is a special event box drawer that overrides the background drawing and fuzzy
    edges drawing of the DefaultEventBoxDrawer.
    """
    def __init__(self, fuzzy_edges=False):
        """
        :param fuzzy_edges: If True, fuzzy edges are drawn instead of using an icon.
        """
        self._fuzzy_edges = fuzzy_edges
        self._event = None
        self._rect = None
        self._light_color = None
        self._dark_color = None

    @mark.overrides
    def _draw_background(self, dc, rect, event):
        """
        :param dc: The device context to draw on
        :param rect: The bounding rectangle where the event shall be drawn.
        :param event: The event to draw
        """
        self._event = event
        self._rect = rect
        self._light_color = lighten_color(self._event.get_color())
        self._dark_color = darken_color(self._event.get_color(), factor=0.8)
        dc.SetPen(self._get_pen(dc, event))
        if self._fuzzy_edges and event.get_fuzzy():
            self._draw_background_and_fuzzy_edges(dc)
        else:
            self._draw_background_no_fuzzy_edges(dc)

    @mark.overrides
    def _draw_fuzzy_edges(self, dc, rect, event):
        """
        :param dc: The device context to draw on
        :param rect: The bounding rectangle where the event shall be drawn.
        :param event: The event to draw
        The purpose of this function is to NOT draw the fuzzy edges icon, since this
        drawer has no left and right edges if self._fuzzy_edges, otherwise we delagate
        all drawing to the DefaultEventBoxDrawer.
        """
        if not self._fuzzy_edges:
            super(OtherGradientEventBoxDrawer, self)._draw_fuzzy_edges(dc, rect, event)

    def _draw_background_no_fuzzy_edges(self, dc):
        dc.DrawRectangle(self._rect)
        dc.GradientFillLinear(decrease_rect_size(self._rect, 1, 1), self._light_color, self._dark_color, wx.WEST)

    def _draw_background_and_fuzzy_edges(self, dc):
        dc.DrawLine(self._rect.GetTopLeft(), self._rect.GetTopRight())
        dc.DrawLine(self._rect.GetBottomLeft(), self._rect.GetBottomRight())
        dc.GradientFillLinear(left_half_of_rect(self._rect), wx.WHITE, self._dark_color, wx.EAST)
        dc.GradientFillLinear(right_half_of_rect(self._rect), wx.WHITE, self._dark_color, wx.WEST)


def decrease_rect_size(rect, dx=1, dy=1):
    return wx.Rect(*rect).Deflate(dx, dy)


def left_half_of_rect(rect):
    r = decrease_rect_size(rect, dx=1, dy=1)
    r.SetWidth(r.GetWidth() // 2)
    return r


def right_half_of_rect(rect):
    r = decrease_rect_size(rect, dx=1, dy=1)
    r.SetWidth(r.GetWidth() // 2)
    r.SetPosition(wx.Point(r.GetX() + r.GetWidth(), r.GetY()))
    return r
