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

from timelinelib.canvas.move import MoveByDragInputHandler
from timelinelib.canvas.timelinecanvascontroller import TimelineCanvasController
from timelinelib.canvas.timelinecanvas import TimelineCanvas
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with, human_time_to_gregorian, gregorian_period
from timelinelib.wxgui.frames.mainframe.mainframe import StatusBarAdapter


class MoveByDragInputHandlerSpec(UnitTestCase):

    def test_moves_point_events(self):
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(self.a_point_event("1 Jan 2011"),
                         from_time="1 Jan 2011", to_x=50)
        self.assert_event_has_period("5 Jan 2011", "5 Jan 2011")

    def test_moves_period_events(self):
        self.given_no_snap()
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(self.a_period_event("1 Jan 2011", "3 Jan 2011"),
                         from_time="3 Jan 2011", to_x=50)
        self.assert_event_has_period("3 Jan 2011", "5 Jan 2011")

    def test_snaps_period_events_to_the_left(self):
        self.given_snaps("3 Jan 2011", "4 Jan 2011")
        self.given_snaps("4 Jan 2011", "6 Jan 2011")
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(self.a_period_event("1 Jan 2011", "2 Jan 2011"),
                         from_time="3 Jan 2011", to_x=50)
        self.assert_event_has_period("4 Jan 2011", "5 Jan 2011")

    def test_snaps_period_events_to_the_right(self):
        self.given_snaps("3 Jan 2011", "3 Jan 2011")
        self.given_snaps("4 Jan 2011", "6 Jan 2011")
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(self.a_period_event("1 Jan 2011", "2 Jan 2011"),
                         from_time="3 Jan 2011", to_x=50)
        self.assert_event_has_period("5 Jan 2011", "6 Jan 2011")

    def test_moves_all_selected_events(self):
        event_1 = self.a_point_event("1 Jan 2011")
        event_2 = self.a_point_event("2 Jan 2011")
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(event_1, from_time="1 Jan 2011", to_x=50)
        self.assert_event_has_period("5 Jan 2011", "5 Jan 2011", event_1)
        self.assert_event_has_period("6 Jan 2011", "6 Jan 2011", event_2)

    def test_moves_no_events_if_one_is_locked(self):
        event_1 = self.a_point_event("1 Jan 2011")
        event_2 = self.a_point_event("2 Jan 2011")
        event_2.set_locked(True)
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(event_1, from_time="1 Jan 2011", to_x=50)
        self.assert_event_has_period("1 Jan 2011", "1 Jan 2011", event_1)
        self.assert_event_has_period("2 Jan 2011", "2 Jan 2011", event_2)

    def test_informs_user_through_hint_why_locked_events_cant_be_moved(self):
        event_1 = self.a_point_event("1 Jan 2011")
        event_2 = self.a_point_event("2 Jan 2011")
        event_2.set_locked(True)
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(event_1, from_time="1 Jan 2011", to_x=50)
        self.assertTrue(self.controller.post_hint_event.called)

    def test_clears_hint_when_done_moving(self):
        self.when_move_done()
        self.controller.post_hint_event.assert_called_with("")

    def test_redraws_timeline_after_move(self):
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(self.a_point_event("1 Jan 2011"),
                         from_time="1 Jan 2011", to_x=50)
        self.assertTrue(self.timeline_canvas.Redraw.called)

    def setUp(self):
        def x(time):
            for key in self.snap_times.keys():
                if key == time:
                    return self.snap_times[key]
            raise KeyError()
        self.times_at = {}
        self.period_events = []
        self.snap_times = {}
        self.selected_events = []
        self.controller = Mock(TimelineCanvasController)
        self.controller.timeline = None
        self.controller.view = Mock()
        self.controller.drawing_algorithm = Mock()
        self.controller.view_properties = Mock()
        self.controller.appearance = Mock()
        self.timeline_canvas = Mock(TimelineCanvas)
        self.timeline_canvas.GetSizeTuple.return_value = (0, 0)
        self.timeline_canvas.GetSelectedEvents.return_value = self.selected_events
        self.timeline_canvas.Snap.side_effect = x
        self.timeline_canvas.GetTimeAt.side_effect = lambda x: self.times_at[x]
        self.timeline_canvas.EventIsPeriod.side_effect = lambda event: event in self.period_events

    def a_point_event(self, time):
        event = an_event_with(time=time)
        self.selected_events.append(event)
        return event

    def a_period_event(self, start, end):
        event = an_event_with(start=start, end=end)
        self.selected_events.append(event)
        return event

    def given_snaps(self, from_, to):
        self.snap_times[human_time_to_gregorian(from_)] = human_time_to_gregorian(to)

    def given_no_snap(self):
        self.timeline_canvas.Snap.side_effect = lambda x: x

    def given_time_at_x_is(self, x, time):
        self.times_at[x] = human_time_to_gregorian(time)

    def when_moving(self, event, from_time, to_x):
        self.moved_event = event
        if event.is_period():
            self.period_events.append(event)
        handler = MoveByDragInputHandler(
            self.timeline_canvas,
            self.controller, event, human_time_to_gregorian(from_time))
        handler.mouse_moved(to_x, 10)

    def when_move_done(self):
        handler = MoveByDragInputHandler(
            self.timeline_canvas,
            self.controller, self.a_point_event("1 Jan 2011"), None)
        handler.left_mouse_up()

    def assert_event_has_period(self, start, end, event=None):
        if event is None:
            event = self.selected_events[0]
        self.assertEqual(event.get_time_period(), gregorian_period(start, end))
