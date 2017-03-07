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

"""
This class represents the legend rectangle drawn on the
:doc:`TimelinePanel <timelinelib_wxgui_components_timelinepanel>`.
It's tests are found :doc:`Here <unit_canvas_drawing_legend>`
"""


from timelinelib.canvas.drawing.utils import darken_color


MARGIN = 5
INNER_PADDING = 3  # Space inside event box to text (pixels)
BOTTOM_LEFT = 0
TOP_LEFT = 1
TOP_RIGHT = 2
BOTTOM_RIGHT = 3


class Legend(object):

    def __init__(self, rect=None, itemheight=None, categories=None, width=0, height=0):
        self._rect = rect
        self._categories = categories
        self._itemheight = itemheight
        self._width = width
        self._height = height
        self.pos = BOTTOM_LEFT

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect


    @property
    def pos(self):
        return self.pos

    @pos.setter
    def pos(self, pos):
        if pos == BOTTOM_LEFT:
            self._rect.SetX(MARGIN)
            self._rect.SetY(self._height - self._rect.height - MARGIN)
        elif pos == TOP_LEFT:
            self._rect.SetX(MARGIN)
            self._rect.SetY(MARGIN)
        elif pos == TOP_RIGHT:
            self._rect.SetX(self._width - self._rect.width - MARGIN)
            self._rect.SetY(MARGIN)
        elif pos == BOTTOM_RIGHT:
            self._rect.SetX(self._width - self._rect.width - MARGIN)
            self._rect.SetY(self._height - self._rect.height - MARGIN)
        self._pos = pos

    @property
    def items(self):
        self.x = self._rect.x + self._rect.Width - self._itemheight - INNER_PADDING
        self.y = self._rect.y + INNER_PADDING
        def c(cat):
            color_box_rect = (self.x, self.y, self._itemheight, self._itemheight)
            dat = (cat.name, cat.color, darken_color(cat.color), self._rect.x + INNER_PADDING, self.y, color_box_rect)
            self.y += self._itemheight + INNER_PADDING
            return dat
        return [c(cat) for cat in self._categories]
