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


class NoopMouseMoved(NoopBaseHandler):

    def __init__(self, canvas, cursor, keyboard):
        NoopBaseHandler.__init__(self, canvas, cursor, keyboard)
        self._show_timer_running = False
        self._hide_timer_running = False

    def run(self, status_bar):

        def select_cursor_shape():

            def over_resize_handle():
                return self.hit_resize_handle() is not None

            def over_move_handle():
                return self.hit_move_handle() and not self.event_at_cursor().get_ends_today()

            methods = MethodContainer(
                [
                    (over_resize_handle(), self._canvas.set_size_cursor),
                    (over_move_handle(), self._canvas.set_move_cursor)
                ],
                default_method=self._canvas.set_default_cursor)
            methods.select(True)()

        select_cursor_shape()
