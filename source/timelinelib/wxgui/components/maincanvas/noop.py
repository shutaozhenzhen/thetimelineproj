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


from timelinelib.general.methodcontainer import MethodContainer
from timelinelib.wxgui.components.maincanvas.inputhandler import InputHandler
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard


"""
A NoOpInputHandler gets messages about the start of a user input, such as a
mouse move action, and delegates the workload to fulfill the user action, to
another event handler
"""


class NoOpInputHandler(InputHandler):

    def __init__(self, state, status_bar, main_frame, timeline_canvas):
        InputHandler.__init__(self, timeline_canvas)
        self._state = state
        self._status_bar = status_bar
        self._main_frame = main_frame
        self.show_timer_running = False
        self.hide_timer_running = False
        self.last_hovered_event = None
        self.last_hovered_balloon_event = None
        self._cursor = None
        self._keyboard = None

    def mouse_moved(self, x, y, alt_down=False):
        self._cursor = Cursor(x, y)
        self._keyboard = Keyboard(False, False, alt_down)
        self.last_hovered_event = self._event_at_cursor()
        self.last_hovered_balloon_event = self._balloon_at_cursor()
        self._start_balloon_timers()
        self._display_info_in_statusbar(self.last_hovered_event)
        self._select_cursor_shape()

    def left_mouse_down(self, x, y, ctrl_down, shift_down, alt_down=False):

        def cursor_over_event():
            return self._event_at_cursor() is not None

        self._cursor = Cursor(x, y)
        self._keyboard = Keyboard(ctrl_down, shift_down, alt_down)
        self._toggle_balloon_stickyness()
        if cursor_over_event():
            self._left_mouse_down_on_event()
        else:
            self._left_mouse_down_on_timeline()

    def left_mouse_dclick(self, x, y, ctrl_down, alt_down=False):
        """
        Event handler used when the left mouse button has been double clicked.

        If the timeline is readonly, no action is taken.
        If the mouse hits an event, a dialog opens for editing this event.
        Otherwise a dialog for creating a new event is opened.
        """
        if self.timeline_canvas.GetDb().is_read_only():
            return
        # Since the event sequence is, 1. EVT_LEFT_DOWN  2. EVT_LEFT_UP
        # 3. EVT_LEFT_DCLICK we must compensate for the toggle_event_selection
        # that occurs in the handling of EVT_LEFT_DOWN, since we still want
        # the event(s) selected or deselected after a left doubleclick
        # It doesn't look too god but I havent found any other way to do it.
        self._cursor = Cursor(x, y)
        self._keyboard = Keyboard(ctrl_down, False, alt_down)
        self._toggle_event_selection()

    def middle_mouse_down(self, x):
        self._cursor = Cursor(x, 0)
        self._navigate()

    def mouse_wheel_moved(self, rotation, ctrl_down, shift_down, alt_down, x):
        self._cursor = Cursor(x, 0)
        self._keyboard = Keyboard(ctrl_down, shift_down, alt_down)
        self._on_wheel_rotated(rotation)

    def _select_cursor_shape(self):

        def over_resize_handle():
            return self._hit_resize_handle() is not None

        def over_move_handle():
            return self._hit_move_handle() and not self.last_hovered_event.get_ends_today()

        methods = MethodContainer(
            [
                (over_resize_handle(), self.timeline_canvas.set_size_cursor),
                (over_move_handle(), self.timeline_canvas.set_move_cursor)
            ],
            default_method=self.timeline_canvas.set_default_cursor)
        methods.select(True)()

    def _left_mouse_down_on_event(self):

        def is_resize_command():
            return self._hit_resize_handle() is not None

        def is_move_command():
            if self._event_at_cursor().get_ends_today():
                return False
            else:
                return self._hit_move_handle()

        def start_event_action(action_method, action_arg):
            if self._main_frame.ok_to_edit():
                try:
                    action_method(self._event_at_cursor(), action_arg)
                except:
                    self._main_frame.edit_ends()
                    raise

        def resize_event():
            start_event_action(
                self._state.change_to_resize_by_drag,
                self._hit_resize_handle())

        def move_event():
            start_event_action(
                self._state.change_to_move_by_drag,
                self._time_at_cursor())

        methods = MethodContainer(
            [
                (is_resize_command(), resize_event),
                (is_move_command(), move_event)
            ],
            default_method=self._toggle_event_selection)
        methods.select(True)()

    def _left_mouse_down_on_timeline(self):
        methods = MethodContainer(
            [
                (Keyboard.NONE, self._scroll),
                (Keyboard.ALT, self._select),
                (Keyboard.SHIFT, self._zoom),
                (Keyboard.CTRL, self._create_event)
            ])
        methods.select(self._keyboard.keys_combination)()

    def _scroll(self):
        self._state.change_to_scroll_by_drag(self._time_at_cursor(), self._cursor.y)

    def _create_event(self):
        self.timeline_canvas.ClearSelectedEvents()
        self._state.change_to_create_period_event_by_drag(self._time_at_cursor())

    def _zoom(self):
        self.timeline_canvas.ClearSelectedEvents()
        self._state.change_to_zoom_by_drag(self._time_at_cursor())

    def _select(self):
        self._state.change_to_select(self._cursor)

    def _noop(self):
        pass

    def _toggle_balloon_stickyness(self):
        event_with_balloon = self._balloon_at_cursor()
        if event_with_balloon:
            self.timeline_canvas.toggle_balloon_stickyness(event_with_balloon)

    def _display_info_in_statusbar(self, event):
        if event is None:
            info_text = self.timeline_canvas.format_current_pos_time_string(self._cursor.x)
        else:
            info_text = event.get_label(self.timeline_canvas.GetTimeType())
        self._status_bar.set_text(info_text)

    def _start_balloon_timers(self):
        if self._balloons_disabled():
            return
        if self._current_event_selected():
            return
        if self.show_timer_running:
            return
        if self.hide_timer_running:
            return
        if self._should_start_balloon_show_timer():
            self.timeline_canvas.start_balloon_show_timer(milliseconds=500, oneShot=True)
            self.show_timer_running = True
        elif self._should_start_balloon_hide_timer():
            self.timeline_canvas.start_balloon_hide_timer(milliseconds=100, oneShot=True)
            self.hide_timer_running = True

    def _current_event_selected(self):
        return (self.last_hovered_event is not None and
                self.timeline_canvas.IsEventSelected(self.last_hovered_event))

    def _should_start_balloon_show_timer(self):
        return (self._mouse_is_over_event() and
                not self._mouse_is_over_balloon() and
                not self._balloon_shown_for_event(self.last_hovered_event))

    def _should_start_balloon_hide_timer(self):
        return (self._balloon_is_shown() and
                not self._mouse_is_over_event() and
                not self._balloon_shown_for_event(self.last_hovered_balloon_event))

    def _mouse_is_over_event(self):
        return self.last_hovered_event is not None

    def _mouse_is_over_balloon(self):
        return self.last_hovered_balloon_event is not None

    def balloon_show_timer_fired(self):
        self.show_timer_running = False
        self._redraw_balloons(self.last_hovered_event)

    def balloon_hide_timer_fired(self):
        self.hide_timer_running = False
        hevt = self.timeline_canvas.GetHoveredEvent()
        # If there is no balloon visible we don't have to do anything
        if hevt is None:
            return
        cevt = self.last_hovered_event
        bevt = self.last_hovered_balloon_event
        # If the visible balloon doesn't belong to the event pointed to
        # we remove the ballloon.
        if hevt != cevt and hevt != bevt:
            self._redraw_balloons(None)

    #
    # Actions delegated to canvas object
    #

    def _toggle_event_selection(self):
        self.timeline_canvas.toggle_event_selection(self._cursor, self._keyboard)

    def _redraw_balloons(self, event):
        self.timeline_canvas.SetHoveredEvent(event)

    def _on_wheel_rotated(self, rotation):
        self.timeline_canvas.on_mouse_wheel_rotated(rotation, self._cursor, self._keyboard)

    def _navigate(self):
        time = self.timeline_canvas.GetTimeAt(self._cursor.x)
        self.timeline_canvas.Navigate(lambda tp: tp.center(time))

    #
    # Getters delegated to canvas object
    #

    def _hit_move_handle(self):
        return self.timeline_canvas.hit_move_handle(self._cursor, self._keyboard)

    def _hit_resize_handle(self):
        return self.timeline_canvas.hit_resize_handle(self._cursor, self._keyboard)

    def _balloon_is_shown(self):
        return self.timeline_canvas.GetHoveredEvent() is not None

    def _balloon_shown_for_event(self, event):
        return self.timeline_canvas.GetHoveredEvent() == event

    def _balloons_disabled(self):
        return not self.timeline_canvas.GetAppearance().get_balloons_visible()

    def _event_at_cursor(self):
        return self.timeline_canvas.GetEventAt(self._cursor, self._keyboard.alt)

    def _balloon_at_cursor(self):
        return self.timeline_canvas.GetBalloonAt(self._cursor)

    def _time_at_cursor(self):
        return self.timeline_canvas.GetTimeAt(self._cursor.x)
