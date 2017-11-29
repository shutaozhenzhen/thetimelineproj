# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


from timelinelib.wxgui.components.maincanvas.noophandlers.noopbase import NoopBaseHandler
from timelinelib.general.methodcontainer import MethodContainer
from timelinelib.wxgui.keyboard import Keyboard


class NoopMouseWheelHandler(NoopBaseHandler):

    def __init__(self, canvas, cursor, keyboard):
        NoopBaseHandler.__init__(self, canvas, cursor, keyboard)

    def handle(self, rotation):
        self._direction = _step_function(rotation)
        methods = MethodContainer(
            [
                (Keyboard.CTRL, self._zoom),
                (Keyboard.SHIFT + Keyboard.CTRL, self._scroll_vertically),
                (Keyboard.SHIFT, self._set_divider_pos),
                (Keyboard.ALT, self._set_event_text_font),
            ]
            , default_method=self._scroll
        )
        methods.select(self._keyboard.keys_combination)()

    def _zoom(self):
        self._canvas.Zoom(self._direction, self._cursor.x)

    def _scroll_vertically(self):
        self._canvas.Scrollvertically(self._direction)

    def _set_divider_pos(self):
        self._canvas.SetDividerPosition(self._canvas.GetDividerPosition() + self._direction)

    def _set_event_text_font(self):
        if self._direction > 0:
            self._canvas.IncrementEventTextFont()
        else:
            self._canvas.DecrementEventTextFont()

    def _scroll(self):
        self._canvas.Scroll(self._direction * 0.1)


def _step_function(x_value):
    y_value = 0
    if x_value < 0:
        y_value = -1
    elif x_value > 0:
        y_value = 1
    return y_value
