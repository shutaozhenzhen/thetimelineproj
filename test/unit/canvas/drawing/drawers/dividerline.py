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


from timelinelib.test.cases.drawers import describe_drawers, TEXT_HEIGHT
import wx


SCENE_HEIGHT = 50
SCENE_DIVIDER_Y = 25
SCENE_WIDTH = 100


class describe_dividerline(describe_drawers):

    def test_can_draw_line_at_divider(self):
        self._drawer.draw_at_divider()
        self._assert_common_values()
        self.assertEqual(SCENE_DIVIDER_Y, self._dc.y1)
        self.assertEqual(SCENE_DIVIDER_Y, self._dc.y2)

    def test_can_draw_line_at_top(self):
        self._drawer.draw_at_top()
        self._assert_common_values()
        self.assertEqual(2 * TEXT_HEIGHT + 2, self._dc.y1)
        self.assertEqual(2 * TEXT_HEIGHT + 2, self._dc.y2)

    def test_can_draw_line_at_bottom(self):
        self._drawer.draw_at_bottom()
        self._assert_common_values()
        self.assertEqual(SCENE_HEIGHT - TEXT_HEIGHT, self._dc.y1)
        self.assertEqual(SCENE_HEIGHT - TEXT_HEIGHT, self._dc.y2)

    def _assert_common_values(self):
        self.assertEqual(1, self._dc.pen_call_count)
        self.assertEqual(1, self._dc.draw_line_call_count)
        self.assertEqual(0, self._dc.x1)
        self.assertEqual(SCENE_WIDTH, self._dc.x2)

    def setUp(self):
        describe_drawers.setUp(self)
        # self.install_gettext() # Needed when test is run standalone
        from timelinelib.canvas.drawing.drawers.dividerline import DividerLine
        self._dc = self.create_dc()
        self._scene = self.create_scene(SCENE_WIDTH, SCENE_HEIGHT, SCENE_DIVIDER_Y)
        self._drawer = DividerLine(Drawer(self._dc, self._scene))


class Drawer:

    def __init__(self, dc, scene):
        self.dc = dc
        self.scene = scene
        self.appearance = Appearance()


class Appearance:

    def get_time_scale_pos(self):
        return 0
