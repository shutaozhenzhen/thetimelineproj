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
from timelinelib.canvas.data.event import Event
from timelinelib.test.cases.unit import UnitTestCase


class describe_svg_drawing_algorithm(UnitTestCase):

    def test_can_draw_divider_line(self):
        shape = self.svg._draw_divider_line()
        self.assertEqual(shape.getXML(), '<line y1="200" x2="400" style="stroke:grey; stroke-width:0.5; " x1="0" y2="200"  />\n')

    def test_can_draw_now_line(self):
        shape = self.svg._draw_now_line()
        self.assertEqual(shape.getXML(), '<line y1="0" x2="150" style="stroke:darkred; stroke-width:1; " x1="150" y2="200"  />\n')

    def test_can_draw_line_to_selected_non_period_event(self):
        self.view_properties.is_selected.return_value = True
        line, circle = self.svg._draw_line_to_non_period_event(self.view_properties, self.point_event, self.point_event_rect)
        self.assertEqual(line.getXML(), '<line y1="106" x2="200" style="stroke:red; stroke-width:1; " x1="200" y2="200"  />\n')
        self.assertEqual(circle.getXML(), '<circle cy="200" cx="200" r="2" style="stroke:black; stroke-width:1; fill:none; "  />\n')

    def test_can_draw_line_to_nonselected_non_period_event(self):
        line, circle = self.svg._draw_line_to_non_period_event(self.view_properties, self.point_event, self.point_event_rect)
        self.assertEqual(line.getXML(), '<line y1="106" x2="200" style="stroke:black; stroke-width:1; " x1="200" y2="200"  />\n')
        self.assertEqual(circle.getXML(), '<circle cy="200" cx="200" r="2" style="stroke:black; stroke-width:1; fill:none; "  />\n')

    def setUp(self):
        path = Mock()
        self.view_properties = self.setup_view_properties()
        self.scene = self.setup_scene()
        self.svg = SVGDrawingAlgorithm(path, self.scene, self.view_properties)

    def setup_view_properties(self):
        view_properties = Mock(ViewProperties)
        view_properties.is_selected.return_value = False
        return view_properties

    def setup_scene(self):
        scene = Mock(TimelineScene)
        scene.width = 400
        scene.height = 200
        scene.divider_y = 200
        scene.x_pos_for_now.return_value = 150
        scene.x_pos_for_time.return_value = 200
        self.point_event = Mock(Event)
        self.point_event_rect = Mock()
        self.point_event_rect.Y = 100
        self.point_event_rect.Height = 12
        scene.event_data = [(self.point_event, self.point_event_rect), ]
        return scene
