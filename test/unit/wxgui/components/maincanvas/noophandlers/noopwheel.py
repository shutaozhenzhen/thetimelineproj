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
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.components.maincanvas.noophandlers.noopwheel import NoopMouseWheelHandler
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.maincanvas import MainCanvas


class describe_noop_base_handler(UnitTestCase):

    def test_holds_canvas(self):
        self.assertEqual(self.canvas, self.handler._canvas)

    def test_holds_cursor(self):
        self.assertEqual(self.cursor, self.handler._cursor)

    def test_holds_keyboard(self):
        self.assertEqual(self.keyboard, self.handler._keyboard)

    def test_when_scrolled_down_and_no_control_keys_the_canvas_is_scrolled_a_tenth_in_the_given_direction(self):
        self.when_mouse_scrolled_down()
        self.canvas.Scroll.assert_called_once_with(0.1)

    def test_when_scrolled_up_and_no_control_keys_the_canvas_is_scrolled_a_tenth_in_the_given_direction(self):
        self.when_mouse_scrolled_up()
        self.canvas.Scroll.assert_called_once_with(-0.1)

    def test_when_scrolled_down_and_shift_key_used_the_divider_position_is_changed(self):
        self.when_keyboard(shift=True)
        self.when_mouse_scrolled_down()
        self.canvas.SetDividerPosition.assert_called_once_with(2)

    def test_when_scrolled_up_and_shift_key_used_the_divider_position_is_changed(self):
        self.when_keyboard(shift=True)
        self.when_mouse_scrolled_up()
        self.canvas.SetDividerPosition.assert_called_once_with(0)

    def test_when_scrolled_down_and_ctrl_used_the_canvas_is_zoomed(self):
        self.when_keyboard(ctrl=True)
        self.when_mouse_scrolled_down()
        self.canvas.Zoom.assert_called_once_with(1, 2)

    def test_when_scrolled_up_and_ctrl_used_the_canvas_is_zoomed(self):
        self.when_keyboard(ctrl=True)
        self.when_mouse_scrolled_up()
        self.canvas.Zoom.assert_called_once_with(-1, 2)

    def test_when_scrolled_down_and_ctrl_shift_the_canvas_is_scrolled_vertically(self):
        self.when_keyboard(ctrl=True, shift=True)
        self.when_mouse_scrolled_down()
        self.canvas.Scrollvertically.assert_called_once_with(1)

    def test_when_scrolled_up_and_ctrl_shift_the_canvas_is_scrolled_vertically(self):
        self.when_keyboard(ctrl=True, shift=True)
        self.when_mouse_scrolled_up()
        self.canvas.Scrollvertically.assert_called_once_with(-1)

    def test_when_scrolled_down_and_alt_used_the_text_font_is_incremented(self):
        self.when_keyboard(alt=True)
        self.when_mouse_scrolled_down()
        self.canvas.IncrementEventTextFont.assert_called_once_with()

    def test_when_scrolled_up_and_alt_used_the_text_font_is_decremented(self):
        self.when_keyboard(alt=True)
        self.when_mouse_scrolled_up()
        self.canvas.DecrementEventTextFont.assert_called_once_with()

    def when_mouse_scrolled_down(self):
        self.handler.handle(100)

    def when_mouse_scrolled_up(self):
        self.handler.handle(-100)

    def when_keyboard(self, ctrl=False, shift=False, alt=False):
        self.handler._keyboard = Keyboard(ctrl, shift, alt)

    def setUp(self):
        self.canvas = Mock(MainCanvas)
        self.canvas.GetDividerPosition.return_value = 1
        self.cursor = Cursor(2, 4)
        self.keyboard = Keyboard(False, False, False)
        self.handler = NoopMouseWheelHandler(self.canvas, self.cursor, self.keyboard)
