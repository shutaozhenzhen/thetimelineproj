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


from timelinelib.wxgui.components.maincanvas.inputhandler import InputHandler
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedown import NoopLeftMouseDown
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedclick import NoopLeftMouseDclick


"""
A NoOpInputHandler gets messages about the start of a user input, such as a
mouse move action, and delegates the workload to fulfill the user action, to
another event handler
"""

LEFT_MOUSE_DOWN = 1
LEFT_MOUSE_DCLICK = 3


def delegates(key, canvas, cursor, keyboard):
    return {LEFT_MOUSE_DOWN: NoopLeftMouseDown,
            LEFT_MOUSE_DCLICK: NoopLeftMouseDclick,
            }[key](canvas, cursor, keyboard)


class NoOpInputHandler(InputHandler):

    def __init__(self, state, status_bar, timeline_canvas, delegates=delegates):
        InputHandler.__init__(self, timeline_canvas)
        self._delegates = delegates
        self._state = state
        self._status_bar = status_bar
        self._cursor = None
        self._keyboard = None

    def left_mouse_down(self, cursor, keyboard):
        delegate = self._delegates(LEFT_MOUSE_DOWN, self._canvas, cursor, keyboard)
        delegate.run(self._state)

    def left_mouse_dclick(self, cursor, keyboard):
        delegate = self._delegates(LEFT_MOUSE_DCLICK, self._canvas, cursor, keyboard)
        delegate.run()
