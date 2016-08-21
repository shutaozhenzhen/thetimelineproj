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


from types import UnicodeType
from xml.sax.saxutils import escape as xmlescape

from pysvg.filter import feGaussianBlur
from pysvg.filter import feOffset
from pysvg.filter import feMerge
from pysvg.filter import feMergeNode
from pysvg.filter import filter
from pysvg.builders import StyleBuilder
from pysvg.builders import ShapeBuilder
from pysvg.structure import g
from pysvg.structure import svg
from pysvg.structure import defs
from pysvg.shape import path
from pysvg.structure import clipPath
from pysvg.text import text

from timelinelib.canvas.drawing.utils import darken_color
from timelinelib.canvas.data import sort_categories


OUTER_PADDING = 5  # Space between event boxes (pixels)
INNER_PADDING = 3  # Space inside event box to text (pixels)
DATA_INDICATOR_SIZE = 10
SMALL_FONT_SIZE_PX = 11
LARGER_FONT_SIZE_PX = 14
ENCODING = "utf-8"


def export(path, timeline, scene, view_properties, appearence):
    svgDrawer = SVGDrawingAlgorithm(path, timeline, scene, view_properties, appearence, shadow=True)
    svgDrawer.draw()
    svgDrawer.write(path)


class SVGDrawingAlgorithm(object):

    # options:  shadow=True|False

    def __init__(self, path, timeline, scene, view_properties, appearence, **kwargs):
        self.path = path
        self.timeline = timeline
        self.scene = scene
        self.appearence = appearence
        self.view_properties = view_properties
        self.svg = svg(width=scene.width, height=scene.height)
        self._small_font_style = self._get_small_font_style()
        self._small_centered_font_style = self._get_small_centered_font_style()
        self._larger_font_style = self._get_larger_font_style()
        try:
            self.shadowFlag = kwargs["shadow"]
        except KeyError:
            self.shadowFlag = False

    def write(self, path):
        """
        write the SVG code into the file with filename path. No
        checking is done if file/path exists
        """
        self.svg.save(path, encoding=ENCODING)

    def draw(self):
        self.svg.addElement(self._define_shadow_filter())
        self.svg.addElement(self._draw_bg())
        for (event, rect) in self.scene.event_data:
            self.svg.addElement(self._draw_event(event, rect))
        categories = self._extract_categories()
        if self._legend_should_be_drawn(self.view_properties, categories):
            self.svg.addElement(self._draw_legend(categories))

    def _draw_bg(self):
        """
        Draw background color
        Draw background Era strips and labels
        Draw major and minor strips, lines to all event boxes and baseline.
        Both major and minor strips have divider lines and labels.
        Draw now line if it is visible
        """
        group = g()
        group.addElement(self._draw_background())
        for era in self.timeline.get_all_periods():
            group.addElement(self._draw_era_strip(era))
            group.addElement(self._draw_era_text(era))
        for strip in self.scene.minor_strip_data:
            group.addElement(self._draw_minor_strip_divider_line(strip.end_time))
            group.addElement(self._draw_minor_strip_label(strip))
        for strip in self.scene.major_strip_data:
            group.addElement(self._draw_major_strip_divider_line(strip.end_time))
            group.addElement(self._draw_major_strip_label(strip))
        group.addElement(self._draw_divider_line())
        self._draw_lines_to_non_period_events(group, self.view_properties)
        if self._now_line_is_visible():
            group.addElement(self._draw_now_line())
        return group

    def _draw_background(self):
        svg_color = self._map_svg_color(self.appearence.get_bg_colour()[:3])
        return ShapeBuilder().createRect(0, 0, self.scene.width, self.scene.height, fill=svg_color)

    def _draw_era_strip(self, era):
        svg_color = self._map_svg_color(era.get_color()[:3])
        x, width = self._calc_era_strip_metrics(era)
        return ShapeBuilder().createRect(x, INNER_PADDING, width,
                                         self.scene.height - 2 * INNER_PADDING,
                                         fill=svg_color, strokewidth=0)

    def _draw_era_text(self, era):
        x, y = self._calc_era_text_metrics(era)
        return self._draw_label(era.get_name(), x, y, self._small_centered_font_style)

    def _calc_era_strip_metrics(self, era):
        period = era.get_time_period()
        x = self.scene.x_pos_for_time(period.start_time)
        width = min(self.scene.x_pos_for_time(period.end_time), self.scene.width) - x
        return x, width

    def _calc_era_text_metrics(self, era):
        period = era.get_time_period()
        _, width = self._calc_era_strip_metrics(era)
        x = self.scene.x_pos_for_time(period.start_time) + width / 2
        y = self.scene.height - OUTER_PADDING
        return x, y

    def _draw_minor_strip_divider_line(self, time):
        return self._draw_vertical_line(self.scene.x_pos_for_time(time), "lightgrey")

    def _draw_minor_strip_label(self, strip_period):
        label = self.scene.minor_strip.label(strip_period.start_time)
        x = self._calc_x_for_minor_strip_label(strip_period)
        y = self._calc_y_for_minor_strip_label()
        return self._draw_label(label, x, y, self._small_font_style)

    def _calc_x_for_minor_strip_label(self, strip_period):
        return (self.scene.x_pos_for_time(strip_period.start_time) +
                self.scene.x_pos_for_time(strip_period.end_time)) / 2 - SMALL_FONT_SIZE_PX

    def _calc_y_for_minor_strip_label(self):
        return self.scene.divider_y - OUTER_PADDING

    def _draw_label(self, label, x, y, style):
        text = self._text(label, x, y)
        text.set_style(style.getStyle())
        return text

    def _draw_major_strip_divider_line(self, time):
        return self._draw_vertical_line(self.scene.x_pos_for_time(time), "black")

    def _draw_vertical_line(self, x, colour):
        return ShapeBuilder().createLine(x, 0, x, self.scene.height, strokewidth=0.5, stroke=colour)

    def _draw_major_strip_label(self, tp):
        label = self.scene.major_strip.label(tp.start_time, True)
        # If the label is not visible when it is positioned in the middle
        # of the period, we move it so that as much of it as possible is
        # visible without crossing strip borders.
        # since there is no function like textwidth() for SVG, just take into account that text can be overwritten
        # do not perform a special handling for right border, SVG is unlimited
        x = (max(0, self.scene.x_pos_for_time(tp.start_time)) +
             min(self.scene.width, self.scene.x_pos_for_time(tp.end_time))) / 2
        y = LARGER_FONT_SIZE_PX + OUTER_PADDING
        return self._draw_label(label, x, y, self._larger_font_style)

    def _draw_divider_line(self):
        return ShapeBuilder().createLine(0, self.scene.divider_y, self.scene.width,
                                         self.scene.divider_y, strokewidth=0.5, stroke="grey")

    def _draw_lines_to_non_period_events(self, group, view_properties):
        for (event, rect) in self.scene.event_data:
            if rect.Y < self.scene.divider_y:
                line, circle = self._draw_line_to_non_period_event(view_properties, event, rect)
                group.addElement(line)
                group.addElement(circle)

    def _draw_line_to_non_period_event(self, view_properties, event, rect):
        x = self.scene.x_pos_for_time(event.mean_time())
        y = rect.Y + rect.Height / 2
        stroke = {True: "red", False: "black"}[view_properties.is_selected(event)]
        line = ShapeBuilder().createLine(x, y, x, self.scene.divider_y, stroke=stroke)
        circle = ShapeBuilder().createCircle(x, self.scene.divider_y, 2)
        return line, circle

    def _draw_now_line(self):
        return self._draw_vertical_line(self.scene.x_pos_for_now(), "darkred")

    def _now_line_is_visible(self):
        x = self.scene.x_pos_for_now()
        return x > 0 and x < self.scene.width

    def _get_event_border_color(self, event):
        return self._map_svg_color(darken_color(self._get_event_color(event)))

    def _get_event_box_color(self, event):
        return self._map_svg_color(self._get_event_color(event))

    def _get_box_indicator_color(self, event):
        return self._map_svg_color(darken_color(self._get_event_color(event), 0.6))

    def _get_event_color(self, event):
        if event.category:
            return event.category.color
        else:
            return event.get_default_color()

    def _map_svg_color(self, color):
        """
        map (r,g,b) color to svg string
        """
        return "#%02X%02X%02X" % color

    def _legend_should_be_drawn(self, view_properties, categories):
        return view_properties.show_legend and len(categories) > 0

    def _extract_categories(self):
        categories = []
        for (event, _) in self.scene.event_data:
            cat = event.category
            if cat and cat not in categories:
                categories.append(cat)
        return sort_categories(categories)

    def _draw_legend(self, categories):
        """
        Draw legend for the given categories.

        Box in lower right corner
            Motivation for positioning in right corner:
            SVG text cannot be centered since the text width cannot be calculated
            and the first part of each event text is important.
            ergo: text needs to be left aligned.
                  But then the probability is high that a lot of text is at the left
                  bottom
                  ergo: put the legend to the right.

          +----------+
          | Name   O |
          | Name   O |
          +----------+
        """
        svgGroup = g()
        svgGroup.addElement(self._draw_categories_box(len(categories)))
        cur_y = self._get_categories_box_y(len(categories)) + OUTER_PADDING
        for cat in categories:
            self._draw_category(self._get_categories_box_width(),
                                self._get_categories_item_height(),
                                self._get_categories_box_x(), svgGroup, cur_y, cat)
            cur_y = cur_y + self._get_categories_item_height() + INNER_PADDING
        return svgGroup

    def _draw_categories_box(self, nbr_of_categories):
        return ShapeBuilder().createRect(self._get_categories_box_x(),
                                         self._get_categories_box_y(nbr_of_categories),
                                         self._get_categories_box_width(),
                                         self._get_categories_box_height(nbr_of_categories),
                                         fill='white')

    def _get_categories_box_width(self):
        # reserve 15% for the legend
        return int(self.scene.width * 0.15)

    def _get_categories_item_height(self):
        return SMALL_FONT_SIZE_PX + OUTER_PADDING

    def _get_categories_box_height(self, nbr_of_categories):
        return nbr_of_categories * (self._get_categories_item_height() + INNER_PADDING) + 2 * OUTER_PADDING - INNER_PADDING

    def _get_categories_box_x(self):
        return self.scene.width - self._get_categories_box_width() - OUTER_PADDING

    def _get_categories_box_y(self, nbr_of_categories):
        return self.scene.height - self._get_categories_box_height(nbr_of_categories) - OUTER_PADDING

    def _draw_category(self, width, item_height, x, svgGroup, cur_y, cat):
        base_color = self._map_svg_color(cat.color)
        border_color = self._map_svg_color(darken_color(cat.color))
        color_box_rect = ShapeBuilder().createRect(x + OUTER_PADDING,
                                                   cur_y, item_height, item_height, fill=base_color,
                                                   stroke=border_color)
        svgGroup.addElement(color_box_rect)
        label = self._svg_clipped_text(cat.name,
                                       (x + OUTER_PADDING + INNER_PADDING + item_height,
                                        cur_y, width - OUTER_PADDING - INNER_PADDING - item_height,
                                        item_height),
                                       self._get_small_font_style())
        svgGroup.addElement(label)

    def _draw_event(self, event, rect):
        if self.scene.center_text():
            style = self._small_centered_font_style
        else:
            style = self._small_font_style
        svgGroup = g()
        svgGroup.addElement(self._draw_event_rect(event, rect))
        svgGroup.addElement(self._svg_clipped_text(event.text, rect.Get(), style,
                                                   self.scene.center_text()))
        if event.has_data():
            svgGroup.addElement(self._draw_contents_indicator(event, rect))
        return svgGroup

    def _draw_event_rect(self, event, rect):
        boxBorderColor = self._get_event_border_color(event)
        svg_rect = ShapeBuilder().createRect(rect.X, rect.Y, rect.GetWidth(), rect.GetHeight(),
                                             stroke=boxBorderColor, fill=self._get_event_box_color(event))
        if self.shadowFlag:
            svg_rect.set_filter("url(#filterShadow)")
        return svg_rect

    def _draw_contents_indicator(self, event, rect):
        """
        The data contents indicator is a small triangle drawn in the upper
        right corner of the event rectangle.
        """
        corner_x = rect.X + rect.Width
        polyPoints = "%d,%d %d,%d %d,%d" % \
            (corner_x - DATA_INDICATOR_SIZE, rect.Y,
             corner_x, rect.Y,
             corner_x, rect.Y + DATA_INDICATOR_SIZE)
        polyColor = self._get_box_indicator_color(event)
        indicator = ShapeBuilder().createPolygon(polyPoints, fill=polyColor, stroke=polyColor)
        # TODO (low): Transparency ?
        return indicator

    def _svg_clipped_text(self, text, rect, style, center_text=False):
        group = g()
        group.set_clip_path("url(#%s)" % self._create_clip_path(rect))
        group.addElement(self._draw_text(text, rect, style, center_text))
        return group

    def _create_clip_path(self, rectTuple):
        path_id, p = self._calc_clip_path(rectTuple)
        clip = clipPath()
        clip.addElement(p)
        clip.set_id(path_id)
        self.svg.addElement(self._create_defs(clip))
        return path_id

    def _calc_clip_path(self, rectTuple):
        rx, ry, width, height = rectTuple
        if rx < 0:
            width += rx
            rx = 0
        pathId = "path%d_%d" % (rx, ry)
        p = path(pathData="M %d %d H %d V %d H %d" %
                 (rx, ry + height, rx + width, ry, rx))
        return pathId, p

    def _draw_text(self, my_text, rect, style, center_text=False):
        my_text = self._encode_text(my_text)
        x, y = self._calc_text_pos(rect, center_text)
        myText = text(my_text, x, y)
        myText.set_style(style.getStyle())
        myText.set_lengthAdjust("spacingAndGlyphs")
        return myText

    def _calc_text_pos(self, rect, center_text=False):
        rx, ry, width, height = rect
        # In SVG, negative value should be OK, but they
        # are not drawn in Firefox. So add a special handling here.
        if rx < 0:
            width += rx
            x = 0
        else:
            x = rx + INNER_PADDING
        if center_text:
            x += (width - 2 * INNER_PADDING) / 2
        y = ry + height - INNER_PADDING
        return x, y

    def _text(self, the_text, x, y):
        encoded_text = self._encode_text(the_text)
        return text(encoded_text, x, y)

    def _encode_text(self, text):
        return self._encode_unicode_text(xmlescape(text))

    def _encode_unicode_text(self, text):
        if type(text) is UnicodeType:
            return text.encode(ENCODING)
        else:
            return text

    def _define_shadow_filter(self):
        return self._create_defs(self._get_shadow_filter())

    def _create_defs(self, definition):
        d = defs()
        d.addElement(definition)
        return d

    def _get_small_font_style(self):
        return self._get_font_style(SMALL_FONT_SIZE_PX, 'left', (2, 2))

    def _get_small_centered_font_style(self):
        return self._get_font_style(SMALL_FONT_SIZE_PX, 'middle', (2, 2))

    def _get_larger_font_style(self):
        return self._get_font_style(LARGER_FONT_SIZE_PX, 'left', "")

    def _get_font_style(self, size, anchor, dash_array):
        myStyle = StyleBuilder()
        myStyle.setStrokeDashArray(dash_array)
        myStyle.setFontFamily(fontfamily="Verdana")
        myStyle.setFontSize("%dpx" % size)
        myStyle.setTextAnchor(anchor)
        return myStyle

    def _get_shadow_filter(self):
        filterShadow = filter(x="-.3", y="-.5", width=1.9, height=1.9)
        filtBlur = feGaussianBlur(stdDeviation="4")
        filtBlur.set_in("SourceAlpha")
        filtBlur.set_result("out1")
        filtOffset = feOffset()
        filtOffset.set_in("out1")
        filtOffset.set_dx(4)
        filtOffset.set_dy(-4)
        filtOffset.set_result("out2")
        filtMergeNode1 = feMergeNode()
        filtMergeNode1.set_in("out2")
        filtMergeNode2 = feMergeNode()
        filtMergeNode2.set_in("SourceGraphic")
        filtMerge = feMerge()
        filtMerge.addElement(filtMergeNode1)
        filtMerge.addElement(filtMergeNode2)
        filterShadow.addElement(filtBlur)  # here i get an error from python. It is not allowed to add a primitive filter
        filterShadow.addElement(filtOffset)
        filterShadow.addElement(filtMerge)
        filterShadow.set_id("filterShadow")
        return filterShadow
