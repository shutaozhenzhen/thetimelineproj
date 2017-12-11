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
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedownontimeline import NoopLeftMouseDownOnTimeline
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedownonevent import NoopLeftMouseDownOnEvent


class NoopLeftMouseDown(NoopBaseHandler):

    def __init__(self, canvas, cursor, keyboard):
        NoopBaseHandler.__init__(self, canvas, cursor, keyboard)

    def run(self, main_frame, state):

        def toggle_balloon_stickyness():
            event_with_balloon = self.balloon_at_cursor()
            if event_with_balloon:
                self._canvas.toggle_balloon_stickyness(event_with_balloon)

        def cursor_over_event():
            return self.event_at_cursor() is not None

        toggle_balloon_stickyness()
        if cursor_over_event():
            self._left_mouse_down_on_event(main_frame, state)
        else:
            self._left_mouse_down_on_timeline(state)

    def _left_mouse_down_on_event(self, main_frame, state):
        delegate = NoopLeftMouseDownOnEvent(self._canvas, self._cursor, self._keyboard)
        delegate.run(state)

    def _left_mouse_down_on_timeline(self, state):
        delegate = NoopLeftMouseDownOnTimeline(self._canvas, self._cursor, self._keyboard)
        delegate.run(state)
