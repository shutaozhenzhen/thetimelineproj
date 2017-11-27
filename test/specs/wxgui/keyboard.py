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


from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.test.cases.unit import UnitTestCase


class describe_keyboard(UnitTestCase):

    def test_has_control_key_proerties(self):
        keyboard = Keyboard(True, True, True)
        self.assertTrue(keyboard.ctrl)
        self.assertTrue(keyboard.shift)
        self.assertTrue(keyboard.alt)

    def test_can_calculate_a_unigue_number_for_each_control_key_combination(self):
        keyboard = Keyboard(True, True, True)
        self.assertEqual(Keyboard.CTRL + Keyboard.SHIFT + Keyboard.ALT, keyboard.keys_combination)
        keyboard = Keyboard(True, True, False)
        self.assertEqual(Keyboard.CTRL + Keyboard.SHIFT, keyboard.keys_combination)
        keyboard = Keyboard(True, False, True)
        self.assertEqual(Keyboard.CTRL + Keyboard.ALT, keyboard.keys_combination)
        keyboard = Keyboard(True, False, False)
        self.assertEqual(Keyboard.CTRL, keyboard.keys_combination)
        keyboard = Keyboard(False, True, True)
        self.assertEqual(Keyboard.SHIFT + Keyboard.ALT, keyboard.keys_combination)
        keyboard = Keyboard(False, True, False)
        self.assertEqual(Keyboard.SHIFT, keyboard.keys_combination)
        keyboard = Keyboard(False, False, True)
        self.assertEqual(Keyboard.ALT, keyboard.keys_combination)
        keyboard = Keyboard(False, False, False)
        self.assertEqual(Keyboard.NONE, keyboard.keys_combination)
