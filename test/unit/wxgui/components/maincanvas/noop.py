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
from mock import Mock
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.noop import NoOpInputHandler
from timelinelib.canvas.data.event import Event
from timelinelib.canvas.data.milestone import Milestone


class describe_hit_resize_handle(UnitTestCase):

    def test_returns_none_when_no_event_is_hit(self):
        self.canvas.GetEventWithHitInfoAt.return_value = None
        self.assertEqual(None, self.handler._hit_resize_handle())

    def test_returns_none_when_a_locked_event_is_hit(self):
        self.canvas.GetEventWithHitInfoAt.return_value = self.a_locked_event(), None
        self.assertEqual(None, self.handler._hit_resize_handle())

    def test_returns_none_when_a_milestone_event_is_hit(self):
        self.canvas.GetEventWithHitInfoAt.return_value = self.a_milestone_event(), None
        self.assertEqual(None, self.handler._hit_resize_handle())

    def test_returns_none_when_the_event_isnt_selected(self):
        self.canvas.GetEventWithHitInfoAt.return_value = self.a_non_selected_event(), None
        self.assertEqual(None, self.handler._hit_resize_handle())

    def test_returns_wxleft_when_selected_event_left_handle_is_hit(self):
        self.canvas.GetEventWithHitInfoAt.return_value = self.a_selected_event(), 1
        self.assertEqual(wx.LEFT, self.handler._hit_resize_handle())

    def test_returns_wxright_when_selected_event_right_handle_is_hit(self):
        self.canvas.GetEventWithHitInfoAt.return_value = self.a_selected_event(), 2
        self.assertEqual(wx.RIGHT, self.handler._hit_resize_handle())

    def test_returns_none_when_selected_event_is_hit_outside_handles(self):
        self.canvas.GetEventWithHitInfoAt.return_value = self.a_selected_event(), 0
        self.assertEqual(None, self.handler._hit_resize_handle())

    def a_locked_event(self):
        evt = Event()
        evt.set_locked(True)
        return evt

    def a_non_selected_event(self):
        self.canvas.IsEventSelected.return_value = False
        return Event()

    def a_selected_event(self):
        self.canvas.IsEventSelected.return_value = True
        return Event()

    def a_milestone_event(self):
        return Milestone()

    def setUp(self):
        self.canvas = Mock()
        self.handler = NoOpInputHandler(None, None, None, self.canvas)
        self.handler._cursor = Cursor(0, 0)
        self.handler._keyboard = Keyboard(False, False, False)
