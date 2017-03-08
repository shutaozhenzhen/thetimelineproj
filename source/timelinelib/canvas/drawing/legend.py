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

    def __init__(self, rect=None, itemheight=None, categories=None, viewport_width=0, viewport_height=0):
        self._rect = rect
        self._categories = categories
        self._itemheight = itemheight
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height
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
        top_y = MARGIN
        bottom_y = self._viewport_height - self._rect.height - MARGIN
        left_x = MARGIN
        right_x = self._viewport_width - self._rect.width - MARGIN
        points = {BOTTOM_LEFT: (left_x, bottom_y),
                  TOP_LEFT: (left_x, top_y),
                  TOP_RIGHT: (right_x, top_y),
                  BOTTOM_RIGHT: (right_x, bottom_y)}
        x, y = points[pos]
        self._rect.SetX(x)
        self._rect.SetY(y)
        self._pos = pos

    @property
    def items(self):
        def c(cat):
            color_box_rect = (self.x, self.y, self._itemheight, self._itemheight)
            dat = (cat.name, cat.color, darken_color(cat.color), self._rect.x + INNER_PADDING, self.y, color_box_rect)
            self.y += self._itemheight + INNER_PADDING
            return dat
        self.x = self._rect.x + self._rect.Width - self._itemheight - INNER_PADDING
        self.y = self._rect.y + INNER_PADDING
        return [c(cat) for cat in self._categories]
