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

        def display_info_in_statusbar():
            event = self.event_at_cursor()
            if event is None:
                info_text = self._canvas.format_current_pos_time_string(self._cursor.x)
            else:
                info_text = event.get_label(self._canvas.GetTimeType())
            status_bar.set_text(info_text)

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

        self._start_balloon_timers()
        display_info_in_statusbar()
        select_cursor_shape()

    def _start_balloon_timers(self):

        def mouse_is_over_event():
            return self.event_at_cursor() is not None

        def mouse_is_over_balloon():
            return self.balloon_at_cursor() is not None

        def should_start_balloon_show_timer():
            return (mouse_is_over_event() and
                    not mouse_is_over_balloon() and
                    not self._balloon_shown_for_event())

        def should_start_balloon_hide_timer():
            return (self._balloon_is_shown() and
                    not mouse_is_over_event() and
                    not self._balloon_shown_for_event())

        if self._balloons_disabled():
            return
        if self._is_selected():
            return
        if self._show_timer_running:
            return
        if self._hide_timer_running:
            return
        if should_start_balloon_show_timer():
            self._canvas.start_balloon_show_timer(milliseconds=500, oneShot=True)
            self._show_timer_running = True
        elif should_start_balloon_hide_timer():
            self._canvas.start_balloon_hide_timer(milliseconds=100, oneShot=True)
            self._hide_timer_running = True

    def _balloon_shown_for_event(self):
        return self._canvas.GetHoveredEvent() == self.event_at_cursor()

    def _balloons_disabled(self):
        return not self._canvas.GetAppearance().get_balloons_visible()

    def _balloon_is_shown(self):
        return self._canvas.GetHoveredEvent() is not None

    def _is_selected(self):
        event = self.event_at_cursor()
        return event is not None and self._canvas.IsEventSelected(event)
