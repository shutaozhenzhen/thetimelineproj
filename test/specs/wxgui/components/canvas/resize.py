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


from unittest.mock import Mock
import wx

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.maincanvas import MainCanvas
from timelinelib.wxgui.components.maincanvas.resizebydrag import ResizeByDragInputHandler


class ResizeEventSpec(UnitTestCase):

    def test_updates_period_on_event(self):
        self.given_time_at_x_is(50, "31 Aug 2010")
        self.when_resizing(an_event_with(time="1 Jan 2010"), wx.RIGHT)
        self.and_moving_mouse_to_x(50)
        self.then_event_gets_period("1 Jan 2010", "31 Aug 2010")

    def test_indicates_a_too_long_event_in_hint(self):
        self.given_time_at_x_is(50, "1 Jan 5000")
        self.when_resizing(an_event_with(time="1 Jan 2000"), wx.RIGHT)
        self.and_moving_mouse_to_x(50)
        self.assertEqual(1, self.state.display_status.call_count)

    def test_clears_hint_if_resize_is_valid(self):
        self.given_time_at_x_is(50, "2 Jan 2000")
        self.when_resizing(an_event_with(time="1 Jan 2000"), wx.RIGHT)
        self.and_moving_mouse_to_x(50)
        self.state.display_status("")

    def test_clears_hint_when_resize_is_done(self):
        self.when_resizing(an_event(), wx.RIGHT)
        self.resizer.left_mouse_up()
        self.state.display_status("")

    def test_changes_input_handler_when_resize_is_done(self):
        self.when_resizing(an_event(), wx.RIGHT)
        self.resizer.left_mouse_up()
        self.state.change_to_no_op.assert_called_with()

    def setUp(self):
        self.db = MemoryDB()
        self.canvas = Mock(MainCanvas)
        self.canvas.GetSize.return_value = (0, 0)
        self.canvas.GetDb.return_value = self.db
        self.state = Mock()
        self.status_bar = Mock()

    def given_time_at_x_is(self, x, time):
        self.canvas.GetTimeAt.return_value = human_time_to_gregorian(time)
        self.canvas.Snap.return_value = human_time_to_gregorian(time)

    def when_resizing(self, event, direction):
        self.event_being_resized = event
        self.db.save_event(event)
        self.resizer = ResizeByDragInputHandler(
            self.state,
            self.canvas,
            event,
            direction
        )

    def and_moving_mouse_to_x(self, x):
        any_y = 10
        self.resizer.mouse_moved(Cursor(x, any_y), Keyboard())

    def then_event_gets_period(self, start, end):
        self.assertEqual(
            gregorian_period(start, end),
            self.event_being_resized.get_time_period()
        )
