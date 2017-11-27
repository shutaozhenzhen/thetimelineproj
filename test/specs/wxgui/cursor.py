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


from timelinelib.wxgui.cursor import Cursor
from timelinelib.test.cases.unit import UnitTestCase


X = 3
Y = 7
XX = 2
YY = 4

class describe_cursor(UnitTestCase):

    def test_has_a_start_pos(self):
        self.assertEqual((X, Y), self.cursor.start)

    def test_has_a_current_pos(self):
        self.assertEqual((X, Y), self.cursor.pos)

    def test_has_a_current_x(self):
        self.assertEqual(X, self.cursor.x)

    def test_has_a_current_y(self):
        self.assertEqual(Y, self.cursor.y)

    def test_current_pos_can_change(self):
        self.cursor.move(XX, YY)
        self.assertEqual((XX, YY), self.cursor.pos)

    def test_start_pos_never_changes(self):
        self.cursor.move(XX, YY)
        self.assertEqual((X, Y), self.cursor.start)

    def test_can_detect_when_last_move_didn_change_the_current_pos(self):
        self.cursor.move(X, Y)
        self.assertFalse(self.cursor.has_moved())

    def test_can_detect_when_last_move_changed_the_current_pos(self):
        self.cursor.move(XX, YY)
        self.assertTrue(self.cursor.has_moved())

    def test_can_reset_the_change_detection(self):
        self.cursor.move(XX, YY)
        self.assertTrue(self.cursor.has_moved())
        self.cursor.reset_move()
        self.assertFalse(self.cursor.has_moved())

    def setUp(self):
        self.cursor = Cursor(X, Y)
