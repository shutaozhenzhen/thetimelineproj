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


import math
import os.path

import wx

from timelinelib.canvas.data import sort_categories
from timelinelib.canvas.data.timeperiod import TimePeriod
from timelinelib.canvas.drawing.drawers.dividerline import DividerLine
from timelinelib.canvas.drawing.drawers.legenddrawer import LegendDrawer
from timelinelib.canvas.drawing.drawers.minorstrip import MinorStripDrawer
from timelinelib.canvas.drawing.drawers.nowline import NowLine
from timelinelib.canvas.drawing.interface import Drawer
from timelinelib.canvas.drawing.scene import TimelineScene
from timelinelib.config.paths import ICONS_DIR
from timelinelib.features.experimental.experimentalfeatures import EXTENDED_CONTAINER_HEIGHT
from timelinelib.utils import unique_based_on_eq
from timelinelib.wxgui.components.font import Font
from wx import BRUSHSTYLE_TRANSPARENT
import timelinelib.wxgui.components.font as font
from timelinelib.canvas.drawing.drawers.ballondrawer import BallonDrawer


OUTER_PADDING = 5  # Space between event boxes (pixels)
INNER_PADDING = 3  # Space inside event box to text (pixels)
PERIOD_THRESHOLD = 20  # Periods smaller than this are drawn as events (pixels)
BALLOON_RADIUS = 12
ARROW_OFFSET = BALLOON_RADIUS + 25
DATA_INDICATOR_SIZE = 10
CONTRAST_RATIO_THREASHOLD = 2250
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class DefaultDrawingAlgorithm(Drawer):

    def __init__(self):
        self._event_text_font = Font(8)
        self._create_pens()
        self._create_brushes()
        self._fixed_ys = {}
        self._do_draw_top_scale = False
        self._do_draw_bottom_scale = True
        self._do_draw_divider_line = False
        self._event_box_drawer = None
        self._background_drawer = None

    def set_event_box_drawer(self, event_box_drawer):
        self._event_box_drawer = event_box_drawer

    def set_background_drawer(self, background_drawer):
        self._background_drawer = background_drawer

    def increment_font_size(self, step=2):
        self._event_text_font.increment(step)
        self._adjust_outer_padding_to_font_size()

    def decrement_font_size(self, step=2):
        if self._event_text_font.GetPointSize() > step:
            self._event_text_font.decrement(step)
            self._adjust_outer_padding_to_font_size()

    def _adjust_outer_padding_to_font_size(self):
        if self._event_text_font.GetPointSize() < 8:
            self.outer_padding = OUTER_PADDING * self._event_text_font.GetPointSize() // 8
        else:
            self.outer_padding = OUTER_PADDING

    def _create_pens(self):
        self.red_solid_pen = wx.Pen(wx.Colour(255, 0, 0), 1, wx.PENSTYLE_SOLID)
        self.black_solid_pen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.PENSTYLE_SOLID)
        self.darkred_solid_pen = wx.Pen(wx.Colour(200, 0, 0), 1, wx.PENSTYLE_SOLID)
        self.minor_strip_pen = wx.Pen(wx.Colour(200, 200, 200), 1, wx.PENSTYLE_USER_DASH)
        self.minor_strip_pen.SetDashes([2, 2])
        self.minor_strip_pen.SetCap(wx.CAP_BUTT)
        self.major_strip_pen = wx.Pen(wx.Colour(200, 200, 200), 1, wx.PENSTYLE_SOLID)
        self.now_pen = wx.Pen(wx.Colour(200, 0, 0), 1, wx.PENSTYLE_SOLID)
        self.red_solid_pen = wx.Pen(wx.Colour(255, 0, 0), 1, wx.PENSTYLE_SOLID)

    def _create_brushes(self):
        self.white_solid_brush = wx.Brush(wx.Colour(255, 255, 255), wx.BRUSHSTYLE_SOLID)
        self.black_solid_brush = wx.Brush(wx.Colour(0, 0, 0), wx.BRUSHSTYLE_SOLID)
        self.red_solid_brush = wx.Brush(wx.Colour(255, 0, 0), wx.BRUSHSTYLE_SOLID)
        self.lightgrey_solid_brush = wx.Brush(wx.Colour(230, 230, 230), wx.BRUSHSTYLE_SOLID)

    def event_is_period(self, time_period):
        period_width_in_pixels = self.scene.width_of_period(time_period)
        return period_width_in_pixels > PERIOD_THRESHOLD

    def _get_text_extent(self, text):
        self.dc.SetFont(self._event_text_font)
        tw, th = self.dc.GetTextExtent(text)
        return tw, th

    def get_closest_overlapping_event(self, event_to_move, up=True):
        return self.scene.get_closest_overlapping_event(event_to_move, up=up)

    def draw(self, dc, timeline, view_properties, appearance, fast_draw=False):
        self.fast_draw = fast_draw
        view_properties.hide_events_done = appearance.get_hide_events_done()
        view_properties._legend_pos = appearance.get_legend_pos()
        view_properties._time_scale_pos = appearance.get_time_scale_pos()
        view_properties.set_fuzzy_icon(appearance.get_fuzzy_icon())
        view_properties.set_locked_icon(appearance.get_locked_icon())
        view_properties.set_hyperlink_icon(appearance.get_hyperlink_icon())
        view_properties.set_skip_s_in_decade_text(appearance.get_skip_s_in_decade_text())
        view_properties.set_display_checkmark_on_events_done(appearance.get_display_checkmark_on_events_done())
        self.minor_strip_pen.SetColour(appearance.get_minor_strip_divider_line_colour())
        self.major_strip_pen.SetColour(appearance.get_major_strip_divider_line_colour())
        self.now_pen.SetColour(appearance.get_now_line_colour())
        self.weekend_color = appearance.get_weekend_colour()
        self.bg_color = appearance.get_bg_colour()
        self.colorize_weekends = appearance.get_colorize_weekends()
        self.outer_padding = OUTER_PADDING
        self.outer_padding = appearance.get_vertical_space_between_events()
        if EXTENDED_CONTAINER_HEIGHT.enabled():
            self.outer_padding += EXTENDED_CONTAINER_HEIGHT.get_extra_outer_padding_to_avoid_vertical_overlapping()
        self.appearance = appearance
        self.dc = dc
        self.time_type = timeline.get_time_type()
        self.scene = self._create_scene(dc.GetSize(), timeline, view_properties, self._get_text_extent)
        if view_properties.use_fixed_event_vertical_pos():
            self._calc_fixed_event_rect_y(dc.GetSize(), timeline, view_properties, self._get_text_extent)
        else:
            self._fixed_ys = {}
        self._perform_drawing(timeline, view_properties)
        del self.dc  # Program crashes if we don't delete the dc reference.

    def _create_scene(self, size, db, view_properties, get_text_extent_fn):
        scene = TimelineScene(size, db, view_properties, get_text_extent_fn, self.appearance)
        scene.set_outer_padding(self.outer_padding)
        scene.set_inner_padding(INNER_PADDING)
        scene.set_period_threshold(PERIOD_THRESHOLD)
        scene.set_data_indicator_size(DATA_INDICATOR_SIZE)
        scene.create()
        return scene

    def _calc_fixed_event_rect_y(self, size, db, view_properties, get_text_extent_fn):
        periods = view_properties.periods
        view_properties.set_displayed_period(TimePeriod(periods[0].start_time, periods[-1].end_time), False)
        large_size = (size[0] * len(periods), size[1])
        scene = self._create_scene(large_size, db, view_properties, get_text_extent_fn)
        for (evt, rect) in scene.event_data:
            self._fixed_ys[evt.id] = rect.GetY()

    def _perform_drawing(self, timeline, view_properties):
        self._background_drawer.draw(
            self, self.dc, self.scene, timeline, self.colorize_weekends, self.weekend_color, self.bg_color)
        if self.fast_draw:
            self._perform_fast_drawing(view_properties)
        else:
            self._perform_normal_drawing(view_properties)

    def _perform_fast_drawing(self, view_properties):
        self._draw_bg()
        self._draw_events(view_properties)
        self._draw_selection_rect(view_properties)

    def _draw_selection_rect(self, view_properties):
        if view_properties._selection_rect:
            self.dc.SetPen(wx.BLACK_PEN)
            self.dc.SetBrush(wx.Brush(wx.WHITE, style=BRUSHSTYLE_TRANSPARENT))
            self.dc.DrawRectangle(*view_properties._selection_rect)

    def _perform_normal_drawing(self, view_properties):
        self._draw_period_selection(view_properties)
        self._draw_bg()
        self._draw_events(view_properties)
        self._draw_legend(view_properties, self._extract_categories())
        self._draw_ballons(view_properties)

    def snap(self, time, snap_region=10):
        if self._distance_to_left_border(time) < snap_region:
            return self._get_time_at_left_border(time)
        elif self._distance_to_right_border(time) < snap_region:
            return self._get_time_at_right_border(time)
        else:
            return time

    def _distance_to_left_border(self, time):
        left_strip_time, _ = self._snap_region(time)
        return self.scene.distance_between_times(time, left_strip_time)

    def _distance_to_right_border(self, time):
        _, right_strip_time = self._snap_region(time)
        return self.scene.distance_between_times(time, right_strip_time)

    def _get_time_at_left_border(self, time):
        left_strip_time, _ = self._snap_region(time)
        return left_strip_time

    def _get_time_at_right_border(self, time):
        _, right_strip_time = self._snap_region(time)
        return right_strip_time

    def _snap_region(self, time):
        left_strip_time = self.scene.minor_strip.start(time)
        right_strip_time = self.scene.minor_strip.increment(left_strip_time)
        return left_strip_time, right_strip_time

    def snap_selection(self, period_selection):
        start, end = period_selection
        return self.snap(start), self.snap(end)

    def event_at(self, x, y, alt_down=False):
        container_event = None
        for (event, rect) in self.scene.event_data:
            if event.is_container():
                rect = self._adjust_container_rect_for_hittest(rect)
            if rect.Contains(wx.Point(x, y)):
                if event.is_container():
                    if alt_down:
                        return event
                    container_event = event
                else:
                    return event
        return container_event

    def get_events_in_rect(self, rect):
        wx_rect = wx.Rect(*rect)
        return [event for (event, rect) in self.scene.event_data if rect.Intersects(wx_rect)]

    def _adjust_container_rect_for_hittest(self, rect):
        if EXTENDED_CONTAINER_HEIGHT.enabled():
            return EXTENDED_CONTAINER_HEIGHT.get_vertical_larger_box_rect(rect)
        else:
            return rect

    def event_with_rect_at(self, x, y, alt_down=False):
        container_event = None
        container_rect = None
        for (event, rect) in self.scene.event_data:
            if rect.Contains(wx.Point(x, y)):
                if event.is_container():
                    if alt_down:
                        return event, rect
                    container_event = event
                    container_rect = rect
                else:
                    return event, rect
        if container_event is None:
            return None
        return container_event, container_rect

    def event_rect(self, evt):
        for (event, rect) in self.scene.event_data:
            if evt == event:
                return rect
        return None

    def balloon_at(self, x, y):
        event = None
        for (event_in_list, rect) in self.balloon_data:
            if rect.Contains(wx.Point(x, y)):
                event = event_in_list
        return event

    def get_time(self, x):
        return self.scene.get_time(x)

    def get_hidden_event_count(self):
        try:
            return self.scene.get_hidden_event_count()
        except AttributeError:
            return 0

    def _draw_period_selection(self, view_properties):
        if not view_properties.period_selection:
            return
        start, end = view_properties.period_selection
        start_x = self.scene.x_pos_for_time(start)
        end_x = self.scene.x_pos_for_time(end)
        self.dc.SetBrush(self.lightgrey_solid_brush)
        self.dc.SetPen(wx.TRANSPARENT_PEN)
        self.dc.DrawRectangle(start_x, 0, end_x - start_x + 1, self.scene.height)

    def _draw_bg(self):
        if self.fast_draw:
            self._draw_fast_bg()
        else:
            self._draw_normal_bg()

    def _draw_fast_bg(self):
        self._draw_minor_strips()
        self._draw_divider_line()

    def _draw_normal_bg(self):
        self._draw_major_strips()
        self._draw_minor_strips()
        self._draw_divider_line()
        self._draw_now_line()

    def _draw_minor_strips(self):
        drawer = MinorStripDrawer(self)
        for strip_period in self.scene.minor_strip_data:
            label = self.scene.minor_strip.label(strip_period.start_time)
            drawer.draw(label, strip_period.start_time, strip_period.end_time)

    def _draw_major_strips(self):
        font.set_major_strip_text_font(self.appearance.get_major_strip_font(), self.dc)
        self.dc.SetPen(self.major_strip_pen)
        self._calculate_use_major_strip_vertical_label()
        for time_period in self.scene.major_strip_data:
            self._draw_major_strip_end_line(time_period)
            self._draw_major_strip_label(time_period)

    def _calculate_use_major_strip_vertical_label(self):
        if len(self.scene.major_strip_data) > 0:
            strip_period = self.scene.major_strip_data[0]
            label = self.scene.major_strip.label(strip_period.start_time, True)
            strip_width = self.scene.width_of_period(strip_period)
            tw, _ = self.dc.GetTextExtent(label)
            self.use_major_strip_vertical_label = strip_width < (tw + 5)
        else:
            self.use_major_strip_vertical_label = False

    def _draw_major_strip_end_line(self, time_period):
        x = self.scene.x_pos_for_time(time_period.end_time)
        self.dc.DrawLine(x, 0, x, self.scene.height)

    def _draw_major_strip_label(self, time_period):
        label = self.scene.major_strip.label(time_period.start_time, True)
        if self.use_major_strip_vertical_label:
            self._draw_major_strip_vertical_label(time_period, label)
        else:
            self._draw_major_strip_horizontal_label(time_period, label)

    def _draw_major_strip_vertical_label(self, time_period, label):
        x = self._calculate_major_strip_vertical_label_x(time_period, label)
        self.dc.DrawRotatedText(label, x, INNER_PADDING, -90)

    def _draw_major_strip_horizontal_label(self, time_period, label):
        x = self._calculate_major_strip_horizontal_label_x(time_period, label)
        self.dc.DrawText(label, x, INNER_PADDING)

    def _calculate_major_strip_horizontal_label_x(self, time_period, label):
        tw, _ = self.dc.GetTextExtent(label)
        x = self.scene.x_pos_for_time(time_period.mean_time()) - tw // 2
        if x - INNER_PADDING < 0:
            x = INNER_PADDING
            right = self.scene.x_pos_for_time(time_period.end_time)
            if x + tw + INNER_PADDING > right:
                x = right - tw - INNER_PADDING
        elif x + tw + INNER_PADDING > self.scene.width:
            x = self.scene.width - tw - INNER_PADDING
            left = self.scene.x_pos_for_time(time_period.start_time)
            if x < left + INNER_PADDING:
                x = left + INNER_PADDING
        return x

    def _calculate_major_strip_vertical_label_x(self, time_period, label):
        _, th = self.dc.GetTextExtent(label)
        return self.scene.x_pos_for_time(time_period.mean_time()) + th // 2

    def _draw_divider_line(self):
        DividerLine(self).draw()

    def _draw_lines_to_non_period_events(self, view_properties):
        for (event, rect) in self.scene.event_data:
            if event.is_milestone():
                continue
            if not event.is_period():
                self._draw_line(view_properties, event, rect)
            elif not self.scene.never_show_period_events_as_point_events() and self._event_displayed_as_point_event(rect):
                self._draw_line(view_properties, event, rect)

    def _event_displayed_as_point_event(self, rect):
        return self.scene.divider_y > rect.Y

    def _draw_line(self, view_properties, event, rect):
        if self.appearance.get_draw_period_events_to_right():
            x = rect.X
        else:
            x = self.scene.x_pos_for_time(event.mean_time())
        y = rect.Y + rect.Height
        y2 = self._get_end_of_line(event)
        self._set_line_color(view_properties, event)
        if event.is_period():
            if self.appearance.get_draw_period_events_to_right():
                x += 1
            self.dc.DrawLine(x - 1, y, x - 1, y2)
            self.dc.DrawLine(x + 1, y, x + 1, y2)
        self.dc.DrawLine(x, y, x, y2)
        self._draw_endpoint(event, x, y2)

    def _draw_endpoint(self, event, x, y):
        if event.get_milestone():
            size = 8
            self.dc.SetBrush(wx.BLUE_BRUSH)
            self.dc.DrawPolygon([wx.Point(-size),
                                 wx.Point(0, -size),
                                 wx.Point(size, 0),
                                 wx.Point(0, size)], x, y)
        else:
            self.dc.DrawCircle(x, y, 2)

    def _get_end_of_line(self, event):
        # Lines are only drawn for events shown as point events and the line length
        # is only dependent on the fact that an event is a subevent or not
        if event.is_subevent():
            y = self._get_container_y(event)
        else:
            y = self.scene.divider_y
        return y

    def _get_container_y(self, subevent):
        for (event, rect) in self.scene.event_data:
            if event.is_container():
                if event is subevent.container:
                    return rect.y - 1
        return self.scene.divider_y

    def _set_line_color(self, view_properties, event):
        if view_properties.is_selected(event):
            self.dc.SetPen(self.red_solid_pen)
            self.dc.SetBrush(self.red_solid_brush)
        else:
            self.dc.SetBrush(self.black_solid_brush)
            self.dc.SetPen(self.black_solid_pen)

    def _draw_now_line(self):
        NowLine(self).draw()

    def _extract_categories(self):
        return sort_categories(unique_based_on_eq(
            event.category
            for (event, _) in self.scene.event_data
            if event.category
        ))

    def _draw_legend(self, view_properties, categories):
        if self._legend_should_be_drawn(categories):
            LegendDrawer(self.dc, self.scene, categories).draw()

    def _legend_should_be_drawn(self, categories):
        return self.appearance.get_legend_visible() and len(categories) > 0

    def _scroll_events_vertically(self, view_properties):
        collection = []
        amount = view_properties.hscroll_amount
        if amount != 0:
            for (event, rect) in self.scene.event_data:
                if rect.Y < self.scene.divider_y:
                    self._scroll_point_events(amount, event, rect, collection)
                else:
                    self._scroll_period_events(amount, event, rect, collection)
            self.scene.event_data = collection

    def _scroll_point_events(self, amount, event, rect, collection):
        rect.Y += amount
        if rect.Y < self.scene.divider_y - rect.height:
            collection.append((event, rect))

    def _scroll_period_events(self, amount, event, rect, collection):
        rect.Y -= amount
        if rect.Y > self.scene.divider_y + rect.height:
            collection.append((event, rect))

    def _draw_events(self, view_properties):
        """Draw all event boxes and the text inside them."""
        self._scroll_events_vertically(view_properties)
        self.dc.DestroyClippingRegion()
        self._draw_lines_to_non_period_events(view_properties)
        for (event, rect) in self.scene.event_data:
            self.dc.SetFont(self._event_text_font)
            if view_properties.use_fixed_event_vertical_pos():
                rect.SetY(self._fixed_ys[event.id])
            if event.is_container():
                self._draw_container(event, rect, view_properties)
            else:
                self._draw_box(rect, event, view_properties)

    def _draw_container(self, event, rect, view_properties):
        box_rect = wx.Rect(rect.X - 2, rect.Y - 2, rect.Width + 4, rect.Height + 4)
        if EXTENDED_CONTAINER_HEIGHT.enabled():
            box_rect = EXTENDED_CONTAINER_HEIGHT.get_vertical_larger_box_rect(rect)
        self._draw_box(box_rect, event, view_properties)

    def _draw_box(self, rect, event, view_properties):
        self.dc.SetClippingRegion(rect)
        self._event_box_drawer.draw(self.dc, self.scene, rect, event, view_properties)
        self.dc.DestroyClippingRegion()

    def _draw_ballons(self, view_properties):
        """Draw ballons on selected events that has 'description' data."""
        self.balloon_data = []  # List of (event, rect)
        top_event = None
        top_rect = None
        self.dc.SetTextForeground(BLACK)
        for (event, rect) in self.scene.event_data:
            if event.get_data("description") is not None or event.get_data("icon") is not None:
                sticky = view_properties.event_has_sticky_balloon(event)
                if view_properties.event_is_hovered(event) or sticky:
                    if not sticky:
                        top_event, top_rect = event, rect
                    self._draw_ballon(event, rect, sticky)
        # Make the unsticky balloon appear on top
        if top_event is not None:
            self._draw_ballon(top_event, top_rect, False)

    def _draw_ballon(self, event, event_rect, sticky):
        """Draw one ballon on a selected event that has 'description' data."""

        def max_text_width(icon_width):
            MIN_TEXT_WIDTH = 200
            SLIDER_WIDTH = 20
            padding = 2 * BALLOON_RADIUS
            if icon_width > 0:
                padding += BALLOON_RADIUS
            else:
                icon_width = 0
            padding += icon_width
            visble_background = self.scene.width - SLIDER_WIDTH
            balloon_width = visble_background - event_rect.X - event_rect.width // 2 + ARROW_OFFSET
            max_text_width = balloon_width - padding
            return max(MIN_TEXT_WIDTH, max_text_width)

        def get_icon_size():
            (iw, ih) = (0, 0)
            icon = event.get_data("icon")
            if icon is not None:
                (iw, ih) = icon.Size
            return iw, ih

        def draw_lines(lines, x, y):
            font_h = self.dc.GetCharHeight()
            ty = y
            for line in lines:
                self.dc.DrawText(line, x, ty)
                ty += font_h

        def adjust_text_x_pos_when_icon_is_present(x):
            icon = event.get_data("icon")
            (iw, _) = get_icon_size()
            if icon is not None:
                return x + iw + BALLOON_RADIUS
            else:
                return x

        def draw_icon(x, y):
            icon = event.get_data("icon")
            if icon is not None:
                self.dc.DrawBitmap(icon, x, y, False)

        def draw_description(lines, x, y):
            if self.appearance.get_text_below_icon():
                iw, ih = get_icon_size()
                if ih > 0:
                    ih += BALLOON_RADIUS // 2
                x -= iw
                y += ih
            if lines is not None:
                x = adjust_text_x_pos_when_icon_is_present(x)
                draw_lines(lines, x, y)

        def get_description_lines(max_text_width, iw):
            description = event.get_data("description")
            if description is not None:
                return break_text(description, self.dc, max_text_width)

        def calc_inner_rect(w, h, max_text_width):
            th = len(lines) * self.dc.GetCharHeight()
            tw = 0
            for line in lines:
                (lw, _) = self.dc.GetTextExtent(line)
                tw = max(lw, tw)
            if event.get_data("icon") is not None:
                w += BALLOON_RADIUS
            w += min(tw, max_text_width)
            h = max(h, th)
            if self.appearance.get_text_below_icon():
                iw, ih = get_icon_size()
                w -= iw
                h = ih + th
            return w, h

        ballon_drawer = BallonDrawer(self.dc)
        (inner_rect_w, inner_rect_h) = (iw, _) = ballon_drawer.get_icon_size(event)
        font.set_balloon_text_font(self.appearance.get_balloon_font(), self.dc)
        max_text_width = max_text_width(iw)
        lines = get_description_lines(max_text_width, iw)
        if lines is not None:
            inner_rect_w, inner_rect_h = calc_inner_rect(inner_rect_w, inner_rect_h, max_text_width)
        MIN_WIDTH = 100
        inner_rect_w = max(MIN_WIDTH, inner_rect_w)
        bounding_rect, x, y = ballon_drawer.draw_balloon_bg((inner_rect_w, inner_rect_h),
                                                            (event_rect.X + event_rect.Width // 2, event_rect.Y),
                                                            True,
                                                            sticky)
        draw_icon(x, y)
        draw_description(lines, x, y)
        # Write data so we know where the balloon was drawn
        # Following two lines can be used when debugging the rectangle
        # self.dc.SetBrush(wx.TRANSPARENT_BRUSH)
        # self.dc.DrawRectangle(bounding_rect)
        self.balloon_data.append((event, bounding_rect))

    def get_period_xpos(self, time_period):
        w, _ = self.dc.GetSize()
        return (max(0, self.scene.x_pos_for_time(time_period.start_time)),
                min(w, self.scene.x_pos_for_time(time_period.end_time)))

    def period_is_visible(self, time_period):
        w, _ = self.dc.GetSize()
        return (self.scene.x_pos_for_time(time_period.start_time) < w and
                self.scene.x_pos_for_time(time_period.end_time) > 0)


def break_text(text, dc, max_width_in_px):
    """ Break the text into lines so that they fits within the given width."""
    sentences = text.split("\n")
    lines = []
    for sentence in sentences:
        w, _ = dc.GetTextExtent(sentence)
        if w <= max_width_in_px:
            lines.append(sentence)
        # The sentence is too long. Break it.
        else:
            break_sentence(dc, lines, sentence, max_width_in_px)
    return lines


def break_sentence(dc, lines, sentence, max_width_in_px):
    """Break a sentence into lines."""
    line = []
    max_word_len_in_ch = get_max_word_length(dc, max_width_in_px)
    words = break_line(dc, sentence, max_word_len_in_ch)
    for word in words:
        w, _ = dc.GetTextExtent("".join(line) + word + " ")
        # Max line length reached. Start a new line
        if w > max_width_in_px:
            lines.append("".join(line))
            line = []
        line.append(word + " ")
        # Word edning with '-' is a broken word. Start a new line
        if word.endswith('-'):
            lines.append("".join(line))
            line = []
    if len(line) > 0:
        lines.append("".join(line))


def break_line(dc, sentence, max_word_len_in_ch):
    """Break a sentence into words."""
    words = sentence.split(" ")
    new_words = []
    for word in words:
        broken_words = break_word(dc, word, max_word_len_in_ch)
        for broken_word in broken_words:
            new_words.append(broken_word)
    return new_words


def break_word(dc, word, max_word_len_in_ch):
    """
    Break words if they are too long.

    If a single word is too long to fit we have to break it.
    If not we just return the word given.
    """
    words = []
    while len(word) > max_word_len_in_ch:
        word1 = word[0:max_word_len_in_ch] + "-"
        word = word[max_word_len_in_ch:]
        words.append(word1)
    words.append(word)
    return words


def get_max_word_length(dc, max_width_in_px):
    TEMPLATE_CHAR = 'K'
    word = [TEMPLATE_CHAR]
    w, _ = dc.GetTextExtent("".join(word))
    while w < max_width_in_px:
        word.append(TEMPLATE_CHAR)
        w, _ = dc.GetTextExtent("".join(word))
    return len(word) - 1
