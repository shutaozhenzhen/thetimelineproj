# -*- coding: utf-8 -*-
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

from timelinelib.canvas.svg import SVGDrawingAlgorithm
from timelinelib.canvas.drawing.scene import TimelineScene
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.canvas.data.event import Event
from timelinelib.canvas.data.era import Era
from timelinelib.test.cases.unit import UnitTestCase


class describe_svg_drawing_algorithm(UnitTestCase):

    def test_can_draw_divider_line(self):
        shape = self.svg._draw_divider_line()
        self.assertEqual(shape.getXML(), '<line y1="200" x2="400" style="stroke:grey; stroke-width:0.5; " x1="0" y2="200"  />\n')

    def test_can_draw_now_line(self):
        shape = self.svg._draw_now_line()
        self.assertEqual(shape.getXML(), '<line y1="0" x2="150" style="stroke:darkred; stroke-width:0.5; " x1="150" y2="200"  />\n')

    def test_can_draw_line_to_selected_non_period_events(self):
        from pysvg.structure import g
        self.view_properties.is_selected.return_value = True
        self.scene.event_data = ((self.point_event, self.point_event_rect),)
        group = g()
        self.svg._draw_lines_to_non_period_events(group, self.view_properties)
        self.assertEqual(group.getXML(), '<g  >\n<line y1="106" x2="200" style="stroke:red; stroke-width:1; " x1="200" y2="200"  />\n<circle cy="200" cx="200" r="2" style="stroke:black; stroke-width:1; fill:none; "  />\n</g>\n')

    def test_can_draw_major_strip_divider_line(self):
        time = Mock()
        self.scene.x_pos_for_time.return_value = 170
        line = self.svg._draw_major_strip_divider_line(time)
        self.assertEqual(line.getXML(), '<line y1="0" x2="170" style="stroke:black; stroke-width:0.5; " x1="170" y2="200"  />\n')

    def test_can_draw_minor_strip_divider_line(self):
        time = Mock()
        self.scene.x_pos_for_time.return_value = 170
        line = self.svg._draw_minor_strip_divider_line(time)
        self.assertEqual(line.getXML(), '<line y1="0" x2="170" style="stroke:lightgrey; stroke-width:0.5; " x1="170" y2="200"  />\n')

    def test_can_draw_line_to_nonselected_non_period_events(self):
        from pysvg.structure import g
        self.scene.event_data = ((self.point_event, self.point_event_rect),)
        group = g()
        self.svg._draw_lines_to_non_period_events(group, self.view_properties)
        self.assertEqual(group.getXML(), '<g  >\n<line y1="106" x2="200" style="stroke:black; stroke-width:1; " x1="200" y2="200"  />\n<circle cy="200" cx="200" r="2" style="stroke:black; stroke-width:1; fill:none; "  />\n</g>\n')

    def test_can_draw_minor_strip_label(self):
        strip = Mock()
        strip.label.return_value = "Label"
        strip_period = Mock()
        self.scene.x_pos_for_time.return_value = 100
        self.scene.minor_strip = strip
        text = self.svg._draw_minor_strip_label(strip_period)
        self.assertEqual(text.getXML(), '<text style="font-size:11px; font-family:Verdana; stroke-dasharray:(2, 2); text-anchor:left; " y="195" x="89"  >\nLabel</text>\n')

    def test_can_draw_major_strip_label(self):
        strip = Mock()
        strip.label.return_value = "2016"
        strip_period = Mock()
        self.scene.x_pos_for_time.return_value = 100
        self.scene.major_strip = strip
        text = self.svg._draw_major_strip_label(strip_period)
        self.assertEqual(text.getXML(), '<text style="font-size:14px; font-family:Verdana; text-anchor:left; " y="19" x="100"  >\n2016</text>\n')

    def test_now_line_is_visible(self):
        self.scene.x_pos_for_now.return_value = 100
        self.assertTrue(self.svg._now_line_is_visible())

    def test_now_line_is_not_visible(self):
        self.scene.x_pos_for_now.return_value = 2000
        self.assertFalse(self.svg._now_line_is_visible())
        self.scene.x_pos_for_now.return_value = -100
        self.assertFalse(self.svg._now_line_is_visible())

    def test_can_draw_event(self):
        event = Mock(Event)
        event.has_data.return_value = True
        event.text = "Foo"
        event.category = None
        event.get_default_color.return_value = (200, 200, 200)
        rect = Mock()
        rect.X = 10
        rect.Y = 20
        rect.Width = 50
        rect.GetWidth.return_value = 50
        rect.GetHeight.return_value = 8
        rect.Get.return_value = (10, 20, 50, 8)
        group = self.svg._draw_event(event, rect)
        self.assertEqual(group.getXML(), '<g  >\n<rect style="stroke:#8C8C8C; stroke-width:1; fill:#C8C8C8; " height="8" width="50" y="20" x="10"  />\n<g clip-path="url(#path10_20_50)"  >\n<text style="font-size:11px; font-family:Verdana; stroke-dasharray:(2, 2); text-anchor:left; " y="25" x="13" lengthAdjust="spacingAndGlyphs"  >\nFoo</text>\n</g>\n<polygon style="stroke:#787878; stroke-width:1; fill:#787878; " points="50,20 60,20 60,30"  />\n</g>\n')

    def test_can_draw_event_with_centered_text(self):
        self.scene.center_text.return_value = True
        event = Mock(Event)
        event.has_data.return_value = True
        event.text = "Foo"
        event.category = None
        event.get_default_color.return_value = (200, 200, 200)
        rect = Mock()
        rect.X = 10
        rect.Y = 20
        rect.Width = 50
        rect.GetWidth.return_value = 50
        rect.GetHeight.return_value = 8
        rect.Get.return_value = (10, 20, 50, 8)
        group = self.svg._draw_event(event, rect)
        self.assertEqual(group.getXML(), '<g  >\n<rect style="stroke:#8C8C8C; stroke-width:1; fill:#C8C8C8; " height="8" width="50" y="20" x="10"  />\n<g clip-path="url(#path10_20_50)"  >\n<text style="font-size:11px; font-family:Verdana; stroke-dasharray:(2, 2); text-anchor:middle; " y="25" x="35" lengthAdjust="spacingAndGlyphs"  >\nFoo</text>\n</g>\n<polygon style="stroke:#787878; stroke-width:1; fill:#787878; " points="50,20 60,20 60,30"  />\n</g>\n')

    def test_can_draw_legend(self):
        category = Mock()
        category.color = (127, 127, 127)
        category.name = "First Category"
        categories = (category,)
        group = self.svg._draw_legend(categories)
        self.assertEqual(group.getXML(), '<g  >\n<rect style="stroke:black; stroke-width:1; fill:white; " height="26" width="60" y="169" x="335"  />\n<rect style="stroke:#585858; stroke-width:1; fill:#7F7F7F; " height="16" width="16" y="174" x="340"  />\n<g clip-path="url(#path359_174_36)"  >\n<text style="font-size:11px; font-family:Verdana; stroke-dasharray:(2, 2); text-anchor:left; " y="187" x="362" lengthAdjust="spacingAndGlyphs"  >\nFirst Category</text>\n</g>\n</g>\n')

    def test_can_define_shadow_filter(self):
        d = self.svg._define_shadow_filter()
        self.assertEqual(d.getXML(), '<defs  >\n<filter height="1.9" width="1.9" y="-.5" x="-.3" id="filterShadow"  >\n<feGaussianBlur result="out1" in="SourceAlpha" stdDeviation="4"  />\n<feOffset dy="-4" result="out2" dx="4" in="out1"  />\n<feMerge  >\n<feMergeNode in="out2"  />\n<feMergeNode in="SourceGraphic"  />\n</feMerge>\n</filter>\n</defs>\n')

    def test__encode_unicode_text(self):
        self.assertEqual("", self.svg._encode_unicode_text(u""))
        self.assertEqual("åäö", self.svg._encode_unicode_text(u"åäö"))

    def test_legend_should_be_drawn(self):
        self.svg._appearence.get_legend_visible.return_value = True
        categories = []
        self.assertFalse(self.svg._legend_should_be_drawn(categories))
        categories = [""]
        self.assertTrue(self.svg._legend_should_be_drawn(categories))
        self.svg._appearence.get_legend_visible.return_value = False
        self.assertFalse(self.svg._legend_should_be_drawn(categories))

    def test_can_get_base_color_when_event_has_no_category(self):
        category = Mock()
        category.color = (1, 2, 3)
        event = Mock()
        event.category = category
        self.assertEqual((1, 2, 3), self.svg._get_event_color(event))

    def test_can_get_base_color_when_event_has_category(self):
        event = Mock()
        event.category = None
        event.get_default_color.return_value = (200, 200, 200)
        self.assertEqual((200, 200, 200), self.svg._get_event_color(event))

    def test_can_draw_background(self):
        self.appearence.get_bg_colour.return_value = (1, 2, 3, 4)
        rect = self.svg._draw_background()
        self.assertEqual(rect.getXML(), '<rect style="stroke:black; stroke-width:1; fill:#010203; " height="200" width="400" y="0" x="0"  />\n')

    def test_can_draw_era_background(self):

        def my_side_effect(*args, **kwargs):
            self.call_count += 1
            if self.call_count == 1:
                return 50
            else:
                return 75

        self.scene.x_pos_for_time.side_effect = my_side_effect
        era = Mock(Era)
        era.get_color.return_value = (127, 127, 127, 4)
        era = self.svg._draw_era_strip(era)
        self.assertEqual(era.getXML(), '<rect style="stroke:black; stroke-width:0; fill:#7F7F7F; " height="194" width="25" y="3" x="50"  />\n')

    def test_can_draw_era_text(self):

        def my_side_effect(*args, **kwargs):
            self.call_count += 1
            if self.call_count == 1:
                return 50
            else:
                return 75

        self.scene.x_pos_for_time.side_effect = my_side_effect
        era = Mock(Era)
        era.get_name.return_value = "foobar"
        text = self.svg._draw_era_text(era)
        self.assertEqual(text.getXML(), '<text style="font-size:11px; font-family:Verdana; stroke-dasharray:(2, 2); text-anchor:middle; " y="195" x="87"  >\nfoobar</text>\n')

    def test_calc_clip_path(self):
        """
             (100, 100)                   (300, 100)
                 X----------------------------X
                 |(103,103)          (297,103)|
                 |  x----------------------x  |
                 |  |                      |  |
                 |  x----------------------x  |
                 | (103,117)         (297,117)|
                 X----------------------------X
             (100, 120)                  (300, 120)
        """
        rect = (100, 100, 200, 20)
        path_id, path = self.svg._calc_clip_path(rect)
        self.assertEqual('path100_100_200', path_id)
        self.assertEqual('<path d="M 100 120 H 300 V 100 H 100 "  />\n', path.getXML())
        rect = (-100, 100, 500, 20)
        path_id, path = self.svg._calc_clip_path(rect)
        self.assertEqual('path0_100_400', path_id)
        self.assertEqual('<path d="M 0 120 H 400 V 100 H 0 "  />\n', path.getXML())

    def test_calc_text_pos(self):
        """
             (100, 100)                   (300, 100)
                 X----------------------------X
                 |(103,103)          (297,103)|
                 |  x----------------------x  |
                 |  |                      |  |
                 |  x----------------------x  |
                 | (103,117)         (297,117)|
                 X----------------------------X
             (100, 120)                  (300, 120)
        """
        rect = (100, 100, 200, 20)
        pos = self.svg._calc_text_pos(rect)
        self.assertEqual((103, 117), pos)
        pos = self.svg._calc_text_pos(rect, center_text=True)
        self.assertEqual((200, 117), pos)
        rect = (-100, 100, 400, 20)
        pos = self.svg._calc_text_pos(rect)
        self.assertEqual((0, 117), pos)
        pos = self.svg._calc_text_pos(rect, center_text=True)
        self.assertEqual((147, 117), pos)

    def setUp(self):
        timeline = Mock()
        self.view_properties = self.setup_view_properties()
        self.appearence = Mock()
        self.scene = self.setup_scene()
        self.svg = SVGDrawingAlgorithm(timeline, self.scene, self.view_properties, self.appearence)

    def setup_view_properties(self):
        view_properties = Mock(ViewProperties)
        view_properties.is_selected.return_value = False
        return view_properties

    def setup_scene(self):
        self.call_count = 0
        scene = Mock(TimelineScene)
        scene.width = 400
        scene.height = 200
        scene.divider_y = 200
        scene.x_pos_for_now.return_value = 150
        scene.x_pos_for_time.return_value = 200
        scene.center_text.return_value = False
        self.point_event = Mock(Event)
        self.point_event_rect = Mock()
        self.point_event_rect.Y = 100
        self.point_event_rect.Height = 12
        scene.event_data = [(self.point_event, self.point_event_rect), ]
        return scene
