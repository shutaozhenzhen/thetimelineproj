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


import wx

from timelinelib.canvas.data import TimeOutOfRangeLeftError
from timelinelib.canvas.data import TimeOutOfRangeRightError
from timelinelib.canvas import TimelineCanvas
from timelinelib.utils import ex_msg
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.inputhandler import InputHandler
from timelinelib.general.methodcontainer import MethodContainer
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.timelinecanvas import LEFT_RESIZE_HANDLE
from timelinelib.canvas.timelinecanvas import RIGHT_RESIZE_HANDLE
from timelinelib.canvas.timelinecanvas import MOVE_HANDLE


class MainCanvas(TimelineCanvas):

    def __init__(self, parent, main_frame, status_bar):
        TimelineCanvas.__init__(self, parent)
        self.main_frame = main_frame
        self._status_bar = status_bar
        self.SetInputHandler(InputHandler(self))
        self.balloon_show_timer = wx.Timer(self, -1)
        self.balloon_hide_timer = wx.Timer(self, -1)
        self.dragscroll_timer = wx.Timer(self, -1)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_left_dclick)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_TIMER, self._on_balloon_show_timer, self.balloon_show_timer)
        self.Bind(wx.EVT_TIMER, self._on_balloon_hide_timer, self.balloon_hide_timer)
        self.Bind(wx.EVT_TIMER, self._on_dragscroll, self.dragscroll_timer)
        self.Bind(wx.EVT_MIDDLE_DOWN, self._on_middle_down)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_mousewheel)

    def SetDb(self, db):
        db.display_in_canvas(self)

    def Navigate(self, navigation_fn):
        try:
            TimelineCanvas.Navigate(self, navigation_fn)
        except (TimeOutOfRangeLeftError) as e:
            self._status_bar.set_text(_("Can't scroll more to the left"))
        except (TimeOutOfRangeRightError) as e:
            self._status_bar.set_text(_("Can't scroll more to the right"))
        except (ValueError, OverflowError) as e:
            self._status_bar.set_text(ex_msg(e))
        else:
            self._status_bar.set_text("")

    def SetInputHandler(self, input_handler):
        self._input_handler = input_handler

    def _on_left_down(self, evt):
        self.main_frame.save_time_period()
        self.SetFocus()
        self._input_handler.left_mouse_down(self._get_cursor(evt),
                                            self._get_keyboard(evt))

    def _on_left_dclick(self, evt):
        self._input_handler.left_mouse_dclick(self._get_cursor(evt),
                                              self._get_keyboard(evt))

    def _get_cursor(self, evt):
        return Cursor(evt.GetX(), evt.GetY())

    def _get_keyboard(self, evt):
        return Keyboard(evt.ControlDown(), evt.ShiftDown(), evt.AltDown())

    def _on_left_up(self, event):
        self._input_handler.left_mouse_up()

    def _on_motion(self, evt):
        self._input_handler.mouse_moved(self._get_cursor(evt),
                                        self._get_keyboard(evt))

    def _on_balloon_show_timer(self, event):
        self._input_handler.balloon_show_timer_fired()

    def _on_balloon_hide_timer(self, event):
        self._input_handler.balloon_hide_timer_fired()

    def _on_dragscroll(self, event):
        self._input_handler.dragscroll_timer_fired()

    def _on_middle_down(self, event):
        self._input_handler.middle_mouse_down(event.GetX())

    def _on_mousewheel(self, evt):
        self.main_frame.save_time_period()
        self._input_handler.mouse_wheel_moved(self._get_cursor(evt),
                                              self._get_keyboard(evt),
                                              evt.GetWheelRotation())

    def start_balloon_show_timer(self, milliseconds=-1, oneShot=False):
        self.balloon_show_timer.Start(milliseconds, oneShot)

    def start_balloon_hide_timer(self, milliseconds=-1, oneShot=False):
        self.balloon_hide_timer.Start(milliseconds, oneShot)

    def start_dragscroll_timer(self, milliseconds=-1, oneShot=False):
        self.dragscroll_timer.Start(milliseconds, oneShot)

    def stop_dragscroll_timer(self):
        self.dragscroll_timer.Stop()

    def on_mouse_wheel_rotated(self, rotation, cursor, keyboard):
        def _zoom(direction):
            self.Zoom(direction, cursor.x)

        def _scroll_vertically(direction):
            self.Scrollvertically(direction)

        def _set_divider_pos(direction):
            self.SetDividerPosition(self.GetDividerPosition() + direction)

        def _set_event_text_font(direction):
            if direction > 0:
                self.IncrementEventTextFont()
            else:
                self.DecrementEventTextFont()

        def _scroll(direction):
            self.Scroll(direction * 0.1)

        methods = MethodContainer(
            [
                (Keyboard.CTRL, _zoom),
                (Keyboard.SHIFT + Keyboard.CTRL, _scroll_vertically),
                (Keyboard.SHIFT, _set_divider_pos),
                (Keyboard.ALT, _set_event_text_font),
            ], default_method=_scroll
        )
        direction = step_function(rotation)
        methods.select(keyboard.keys_combination)(direction)

    def toggle_event_selection(self, cursor, keyboard):

        def toggle_event_selection_when_event_is_hit(event):
            selected = not self.IsEventSelected(event)
            if keyboard.ctrl:
                self.SetEventSelected(event, selected)
            else:
                self.ClearSelectedEvents()
                self.SetEventSelected(event, selected)

        event = self.GetEventAt(cursor, keyboard.alt)
        if event:
            toggle_event_selection_when_event_is_hit(event)
        else:
            self.ClearSelectedEvents()

    def format_current_pos_time_string(self, x):
        tm = self.GetTimeAt(x)
        return self.GetTimeType().format_period(TimePeriod(tm, tm))

    def toggle_balloon_stickyness(self, event_with_balloon):
        stick = not self.EventHasStickyBalloon(event_with_balloon)
        self.SetEventStickyBalloon(event_with_balloon, stick)
        if stick:
            self.Redraw()
        else:
            if self.GetAppearance().get_balloons_visible():
                self.SetHoveredEvent(event_with_balloon)
            else:
                self.SetHoveredEvent(None)

    def hit_resize_handle(self, cursor, keyboard):
        try:
            event, hit_info = self.GetEventWithHitInfoAt(cursor, keyboard)
            if event.get_locked():
                return None
            if event.is_milestone():
                return None
            if not self.IsEventSelected(event):
                return None
            if hit_info == LEFT_RESIZE_HANDLE:
                return wx.LEFT
            if hit_info == RIGHT_RESIZE_HANDLE:
                return wx.RIGHT
            return None
        except:
            return None

    def hit_move_handle(self, cursor, keyboard):
        event_and_hit_info = self.GetEventWithHitInfoAt(cursor, keyboard)
        if event_and_hit_info is None:
            return False
        (event, hit_info) = event_and_hit_info
        if event.get_locked():
            return False
        if not self.IsEventSelected(event):
            return False
        return hit_info == MOVE_HANDLE


def step_function(x_value):
    y_value = 0
    if x_value < 0:
        y_value = -1
    elif x_value > 0:
        y_value = 1
    return y_value
