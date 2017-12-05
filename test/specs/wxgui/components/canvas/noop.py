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


from mock import Mock
import wx

from timelinelib.canvas.timelinecanvas import MOVE_HANDLE
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event, an_event_with, human_time_to_gregorian
from timelinelib.wxgui.components.maincanvas.maincanvas import MainCanvas
from timelinelib.wxgui.components.maincanvas.noop import NoOpInputHandler
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard


class NoOpInputHandlerSpec(UnitTestCase):

    def test_changes_input_handler_to_move_when_pressing_move_handle(self):
        event = an_event()
        time = human_time_to_gregorian("1 Jan 2011")
        self.given_time_at_x_is(10, time)
        self.given_event_with_rect_at(Cursor(10, 10), event, wx.Rect(0, 0, 20, 20))
        self.given_event_selected(event)
        self.canvas.hit_resize_handle.return_value = None
        self.canvas.hit_move_handle.return_value = True
        self.handler.left_mouse_down(Cursor(10, 10), Keyboard(False, False, False))
        self.state.change_to_move_by_drag.assert_called_with(event, time)

    def test_disables_move_handler_when_event_ends_today(self):
        event = an_event_with(ends_today=True)
        time = human_time_to_gregorian("1 Jan 2011")
        self.given_time_at_x_is(10, time)
        self.given_event_with_rect_at(Cursor(10, 10), event, wx.Rect(0, 0, 20, 20))
        self.given_event_selected(event)
        self.handler.left_mouse_down(Cursor(10, 10), Keyboard(False, False, False))
        self.assertEqual(0, self.canvas.SetInputHandler.call_count)

    def test_disables_mouse_cursor_when_event_ends_today(self):
        event = an_event_with(ends_today=True)
        time = human_time_to_gregorian("1 Jan 2011")
        self.given_time_at_x_is(10, time)
        self.given_event_with_rect_at(Cursor(10, 10), event, wx.Rect(0, 0, 20, 20))
        self.given_event_selected(event)
        self.handler.mouse_moved(Cursor(10, 10), Keyboard(False, False, False))
        self.assertEqual(0, self.canvas.set_move_cursor.call_count)

    def setUp(self):
        self.setup_timeline_canvas_controller_mock()
        self.canvas = Mock(MainCanvas)
        self.canvas.GetEventAt.side_effect = lambda cursor, alt: self.events_at[(cursor.x, cursor.y)][0]
        self.canvas.GetEventWithHitInfoAt.side_effect = lambda cursor, alt: (self.events_at[(cursor.x, cursor.y)][0], MOVE_HANDLE)
        self.canvas.GetTimeAt.side_effect = lambda x: self.times_at[x]
        self.canvas.GetSelectedEvents.return_value = []
        self.state = Mock()
        self.status_bar = Mock()
        self.main_frame = Mock()
        self.handler = NoOpInputHandler(
            self.state, self.status_bar, self.main_frame, self.canvas)

    def setup_timeline_canvas_controller_mock(self):
        self.times_at = {}
        self.events_at = {}
        self.selected_events = []

    def given_time_at_x_is(self, x, time):
        self.times_at[x] = time

    def given_event_with_rect_at(self, cursor, event, rect):
        self.events_at[(cursor.x, cursor.y)] = (event, rect)

    def given_event_selected(self, event):
        self.selected_events.append(event)
