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
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedown import NoopLeftMouseDown
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedclick import NoopLeftMouseDclick
from timelinelib.wxgui.components.maincanvas.noophandlers.mousemoved import NoopMouseMoved
from timelinelib.wxgui.components.maincanvas.noophandlers.mousewheelmoved import NoopMouseWheelMoved
from timelinelib.wxgui.components.maincanvas.noophandlers.middlemousedown import NoopMiddleMouseDown


"""
A NoOpInputHandler gets messages about the start of a user input, such as a
mouse move action, and delegates the workload to fulfill the user action, to
another event handler
"""


def delegates(key, canvas, cursor, keyboard):
    return {'left_mouse_down': NoopLeftMouseDown,
            'left_mouse_dclick': NoopLeftMouseDclick,
            'mouse_moved': NoopMouseMoved,
            'mouse_wheel_moved': NoopMouseWheelMoved,
            'middle_mouse_down': NoopMiddleMouseDown,
            }[key](canvas, cursor, keyboard)


class NoOpInputHandler(InputHandler):

    def __init__(self, state, status_bar, main_frame, timeline_canvas, delegates=delegates):
        InputHandler.__init__(self, timeline_canvas)
        self._delegates = delegates
        self._state = state
        self._status_bar = status_bar
        self._main_frame = main_frame
        self._cursor = None
        self._keyboard = None

    def mouse_moved(self, cursor, keyboard):
        self._cursor = cursor
        self._keyboard = keyboard
        delegate = self._delegates(self.mouse_moved.__name__,
                                   self.timeline_canvas,
                                   cursor,
                                   keyboard)
        delegate.run(self._status_bar)

    def left_mouse_down(self, cursor, keyboard):
        delegate = self._delegates(self.left_mouse_down.__name__,
                                   self.timeline_canvas,
                                   cursor,
                                   keyboard)
        delegate.run(self._main_frame, self._state)

    def left_mouse_dclick(self, cursor, keyboard):
        delegate = self._delegates(self.left_mouse_dclick.__name__,
                                   self.timeline_canvas,
                                   cursor,
                                   keyboard)
        delegate.run()

    def middle_mouse_down(self, cursor, keyboard):
        delegate = self._delegates(self.middle_mouse_down.__name__,
                                   self.timeline_canvas,
                                   cursor,
                                   keyboard)
        delegate.run()

    def mouse_wheel_moved(self, cursor, keyboard, rotation):
        delegate = self._delegates(self.mouse_wheel_moved.__name__,
                                   self.timeline_canvas,
                                   cursor,
                                   keyboard)
        delegate.run(rotation)

    def balloon_show_timer_fired(self):
        """Callback function that the canvas object fires."""
        self._redraw_balloons()

    def balloon_hide_timer_fired(self):
        """Callback function that the canvas object fires."""
        hevt = self.timeline_canvas.GetHoveredEvent()
        # If there is no balloon visible we don't have to do anything
        if hevt is None:
            return
        cevt = self._event_at_cursor()
        bevt = self.timeline_canvas.GetBalloonAt(self._cursor)
        # If the visible balloon doesn't belong to the event pointed to
        # we remove the ballloon.
        if hevt != cevt and hevt != bevt:
            self._redraw_balloons()

    def _redraw_balloons(self):
        self.timeline_canvas.SetHoveredEvent(self._event_at_cursor())

    def _event_at_cursor(self):
        return self.timeline_canvas.GetEventAt(self._cursor, self._keyboard.alt)
