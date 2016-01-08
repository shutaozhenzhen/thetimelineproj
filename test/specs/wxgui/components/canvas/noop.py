# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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

from timelinelib.canvas.move import MoveByDragInputHandler
from timelinelib.canvas.noop import NoOpInputHandler
from timelinelib.canvas.timelinecanvascontroller import TimelineCanvasController
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event, an_event_with, human_time_to_gregorian
from timelinelib.wxgui.components.timelinepanel import TimelineCanvas


class NoOpInputHandlerSpec(UnitTestCase):

    def test_changes_input_handler_to_move_when_pressing_move_handle(self):
        event = an_event()
        time = human_time_to_gregorian("1 Jan 2011")
        self.given_time_at_x_is(10, time)
        self.given_event_with_rect_at(10, 10, event, wx.Rect(0, 0, 20, 20))
        self.given_event_selected(event)
        self.handler.left_mouse_down(10, 10, False, False)
        self.assertTrue(isinstance(
            self.timeline_canvas.SetInputHandler.call_args[0][0],
            MoveByDragInputHandler))

    def test_disables_move_handler_when_event_ends_today(self):
        event = an_event_with(ends_today=True)
        time = human_time_to_gregorian("1 Jan 2011")
        self.given_time_at_x_is(10, time)
        self.given_event_with_rect_at(10, 10, event, wx.Rect(0, 0, 20, 20))
        self.given_event_selected(event)
        self.handler.left_mouse_down(10, 10, False, False)
        self.assertEqual(0, self.timeline_canvas.SetInputHandler.call_count)

    def test_disables_mouse_cursor_when_event_ends_today(self):
        event = an_event_with(ends_today=True)
        time = human_time_to_gregorian("1 Jan 2011")
        self.given_time_at_x_is(10, time)
        self.given_event_with_rect_at(10, 10, event, wx.Rect(0, 0, 20, 20))
        self.given_event_selected(event)
        self.handler.mouse_moved(10, 10)
        self.assertEqual(0, self.timeline_canvas.set_move_cursor.call_count)

    def setUp(self):
        self.setup_timeline_canvas_controller_mock()
        self.timeline_canvas = Mock(TimelineCanvas)
        self.timeline_canvas.GetEventAt.side_effect = lambda x, y, alt: self.events_at[(x, y)][0]
        self.timeline_canvas.GetTimeAt.side_effect = lambda x: self.times_at[x]
        self.timeline_canvas.GetSelectedEvents.return_value = []
        self.handler = NoOpInputHandler(self.controller, self.timeline_canvas)

    def setup_timeline_canvas_controller_mock(self):
        self.times_at = {}
        self.events_at = {}
        self.selected_events = []
        self.controller = Mock(TimelineCanvasController)
        self.controller.drawing_algorithm = Mock()
        self.controller.view_properties = Mock()
        self.controller.appearance = Mock()
        self.controller.event_with_rect_at.side_effect = lambda x, y, alt: self.events_at[(x, y)]
        self.controller.is_selected.side_effect = lambda event: event in self.selected_events

    def given_time_at_x_is(self, x, time):
        self.times_at[x] = time

    def given_event_with_rect_at(self, x, y, event, rect):
        self.events_at[(x, y)] = (event, rect)

    def given_event_selected(self, event):
        self.selected_events.append(event)
