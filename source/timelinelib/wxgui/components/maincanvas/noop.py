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
# from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedown import NoopLeftMouseDown
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedownontimeline import NoopLeftMouseDownOnTimeline
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedownonevent import NoopLeftMouseDownOnEvent


"""
A NoOpInputHandler gets messages about the start of a user input, such as a
mouse move action, and delegates the workload to fulfill the user action, to
another event handler
"""


class NoOpInputHandler(InputHandler):

    def __init__(self, state, status_bar, timeline_canvas):
        InputHandler.__init__(self, timeline_canvas)
        self._state = state
        self._status_bar = status_bar
        self._cursor = None
        self._keyboard = None

    def left_mouse_down(self, cursor, keyboard):

        def toggle_balloon_stickyness():
            event_with_balloon = self._canvas.GetBalloonAt(self._cursor)
            if event_with_balloon:
                self._canvas.toggle_balloon_stickyness(event_with_balloon)

        def cursor_over_event():
            return self._canvas.GetEventAt(self._cursor, self._keyboard.alt) is not None

        self._cursor = cursor
        self._keyboard = keyboard
        toggle_balloon_stickyness()
        if cursor_over_event():
            self._left_mouse_down_on_event(self._state)
        else:
            self._left_mouse_down_on_timeline(self._state)

    def _left_mouse_down_on_event(self, state):
        delegate = NoopLeftMouseDownOnEvent(self._canvas, self._cursor, self._keyboard)
        delegate.run(state)

    def _left_mouse_down_on_timeline(self, state):
        delegate = NoopLeftMouseDownOnTimeline(self._canvas, self._cursor, self._keyboard)
        delegate.run(state)
