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

from timelinelib.canvas.svg import SVGDrawingAlgorithm
from timelinelib.canvas.drawing.scene import TimelineScene
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.test.cases.unit import UnitTestCase


class describe_svg_drawing_algorithm(UnitTestCase):

    def test_can_draw_divider_line(self):
        shape = self.svg._draw_divider_line()
        self.assertEqual(shape.getXML(), '<line y1="200" x2="400" style="stroke:grey; stroke-width:0.5; " x1="0" y2="200"  />\n')

    def test_can_draw_now_line(self):
        shape = self.svg._draw_now_line()
        self.assertEqual(shape.getXML(), '<line y1="0" x2="150" style="stroke:darkred; stroke-width:1; " x1="150" y2="200"  />\n')

    def setUp(self):
        path = Mock()
        scene = self.setup_scene()
        view_properties = Mock(ViewProperties)
        self.svg = SVGDrawingAlgorithm(path, scene, view_properties)

    def setup_scene(self):
        scene = Mock(TimelineScene)
        scene.width = 400
        scene.height = 200
        scene.divider_y = 200
        scene.x_pos_for_now.return_value = 150
        return scene
