# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
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

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.maincanvas import MainCanvas
from timelinelib.wxgui.components.maincanvas.movebydrag import MoveByDragInputHandler


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
        self.state.display_status.assert_called_with(u"\u27eaCan't move locked event\u27eb")

    def test_clears_hint_when_done_moving(self):
        self.when_move_done()
        self.state.display_status.assert_called_with("")

    def test_redraws_timeline_after_move(self):
        self.given_time_at_x_is(50, "5 Jan 2011")
        self.when_moving(self.a_point_event("1 Jan 2011"), from_time="1 Jan 2011", to_x=50)
        self.assertTrue(self.canvas.Redraw.called)

    def setUp(self):
        def x(time):
            for key in self.snap_times.keys():
                if key == time:
                    return self.snap_times[key]
            raise KeyError()
        self.db = MemoryDB()
        self.times_at = {}
        self.period_events = []
        self.snap_times = {}
        self.selected_events = []
        self.status_bar = Mock()
        self.canvas = Mock(MainCanvas)
        self.canvas.GetDb.return_value = self.db
        self.canvas.GetSizeTuple.return_value = (0, 0)
        self.canvas.GetSelectedEvents.return_value = self.selected_events
        self.canvas.Snap.side_effect = x
        self.canvas.GetTimeAt.side_effect = lambda x: self.times_at[x]
        self.canvas.EventIsPeriod.side_effect = lambda event: event in self.period_events
        self.state = Mock()

    def a_point_event(self, time):
        event = an_event_with(time=time)
        self.selected_events.append(event)
        self.db.save_event(event)
        return event

    def a_period_event(self, start, end):
        event = an_event_with(human_start_time=start, human_end_time=end)
        self.selected_events.append(event)
        self.db.save_event(event)
        return event

    def given_snaps(self, from_, to):
        self.snap_times[human_time_to_gregorian(from_)] = human_time_to_gregorian(to)

    def given_no_snap(self):
        self.canvas.Snap.side_effect = lambda x: x

    def given_time_at_x_is(self, x, time):
        self.times_at[x] = human_time_to_gregorian(time)

    def when_moving(self, event, from_time, to_x):
        self.moved_event = event
        if event.is_period():
            self.period_events.append(event)
        handler = MoveByDragInputHandler(
            self.state,
            self.canvas,
            event,
            human_time_to_gregorian(from_time)
        )
        handler.mouse_moved(Cursor(to_x, 10), Keyboard())

    def when_move_done(self):
        handler = MoveByDragInputHandler(
            self.state,
            self.canvas,
            self.a_point_event("1 Jan 2011"),
            None
        )
        handler.left_mouse_up()

    def assert_event_has_period(self, start, end, event=None):
        if event is None:
            event = self.selected_events[0]
        self.assertEqual(event.get_time_period(), gregorian_period(start, end))
