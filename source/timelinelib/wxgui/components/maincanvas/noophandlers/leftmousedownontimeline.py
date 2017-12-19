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


class NoopLeftMouseDownOnTimeline(NoopBaseHandler):

    def __init__(self, canvas, cursor, keyboard):
        NoopBaseHandler.__init__(self, canvas, cursor, keyboard)

    def run(self, state):

        def scroll():
            state.change_to_scroll_by_drag(self.time_at_cursor(), self._cursor.y)

        def create_event():
            self._canvas.ClearSelectedEvents()
            state.change_to_create_period_event_by_drag(self.time_at_cursor())

        def zoom():
            self._canvas.ClearSelectedEvents()
            state.change_to_zoom_by_drag(self.time_at_cursor())

        def select():
            state.change_to_select(self._cursor)

        methods = MethodContainer(
            [
                (Keyboard.NONE, scroll),
                (Keyboard.ALT, select),
                (Keyboard.SHIFT, zoom),
                (Keyboard.CTRL, create_event)
            ])
        methods.select(self._keyboard.keys_combination)()
