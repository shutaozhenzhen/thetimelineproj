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

LEFT_HANDLE = 'left'
MIDDLE_HANDLE = 'middle'
RIGHT_HANDLE = 'right'


class HandleRect(wx.Rect):
    """
    This class represents the little squared rectangle showing up when an event
    is selected. It's a handle with which you can resize or move the event.
    """

    SIZE = 4

    def __init__(self, rect, pos=MIDDLE_HANDLE):
        wx.Rect.__init__(self, wx.Point(0, 0), wx.Size(self.SIZE, self.SIZE))
        {LEFT_HANDLE: self._translate_to_left_edge,
         MIDDLE_HANDLE: self._translate_to_middle,
         RIGHT_HANDLE: self._translate_to_right_edge}[pos](rect)

    def _translate_to_left_edge(self, rect):
        """
        Translate the handle rectangle to the left edge of the given rectangle

         (rect.X, rect.Y)
              +------------------+
        (x,y) |                  |
            +---+                |
            |   |  ------------- |---------- Center line
            +---+                |
              |                  |
              +------------------+
        """
        x = (2 * (rect.x - self.x) - self.width) // 2
        self.Offset(x, self._get_y(rect))

    def _translate_to_right_edge(self, rect):
        x = (2 * (rect.GetTopRight().x - self.x) - self.width) // 2
        self.Offset(x, self._get_y(rect))

    def _translate_to_middle(self, rect):
        x = (self.x + rect.GetTopLeft().x + rect.GetTopRight().x - self.width) // 2
        self.Offset(x, self._get_y(rect))

    def draw(self, dc):
        dc.SetPen(black_solid_pen(1))
        dc.SetBrush(black_solid_brush())
        dc.DrawRectangle(self)

    def _get_y(self, rect):
        return (self.y + rect.GetTopLeft().y + rect.GetBottomLeft().y - self.height) // 2
