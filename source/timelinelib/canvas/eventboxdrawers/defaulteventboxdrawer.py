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


import os

import wx

from timelinelib.canvas.drawing.utils import black_solid_pen, black_solid_brush, get_colour, darken_color
from timelinelib.config.paths import EVENT_ICONS_DIR
from timelinelib.features.experimental.experimentalfeatures import EXTENDED_CONTAINER_HEIGHT


HANDLE_SIZE = 4
HALF_HANDLE_SIZE = HANDLE_SIZE // 2
DATA_INDICATOR_SIZE = 10
INNER_PADDING = 3  # Space inside event box to text (pixels)
GRAY = (200, 200, 200)


class DefaultEventBoxDrawer(object):

    def draw(self, dc, scene, rect, event, view_properties):
        self.scene = scene
        self.view_properties = view_properties
        selected = view_properties.is_selected(event)
        self.center_text = scene.center_text()
        if event.is_milestone():
            self._draw_milestone_event(dc, rect, event, selected)
        elif scene.never_show_period_events_as_point_events() and rect.y < scene.divider_y and event.is_period():
            self._draw_period_event_as_symbol_below_divider_line(dc, scene, event)
        else:
            self._draw_event_box(dc, rect, event, selected)

    def _draw_period_event_as_symbol_below_divider_line(self, dc, scene, event):
        dc.DestroyClippingRegion()
        x = scene.x_pos_for_time(event.mean_time())
        y0 = scene.divider_y
        y1 = y0 + 10
        dc.SetBrush(black_solid_brush())
        dc.SetPen(black_solid_pen(1))
        dc.DrawLine(x, y0, x, y1)
        dc.DrawCircle(x, y1, 2)

    def _draw_event_box(self, dc, rect, event, selected):
        self._draw_background(dc, rect, event)
        self._draw_fuzzy_edges(dc, rect, event)
        self._draw_locked_edges(dc, rect, event)
        self._draw_progress_box(dc, rect, event)
        self._draw_text(dc, rect, event)
        self._draw_contents_indicator(dc, event, rect)
        self._draw_locked_edges(dc, rect, event)
        self._draw_selection_handles(dc, event, rect, selected)
        self._draw_hyperlink(dc, rect, event)

    def _draw_background(self, dc, rect, event):
        dc.SetBrush(wx.Brush(event.get_color(), wx.BRUSHSTYLE_SOLID))
        dc.SetPen(self._get_pen(dc, event))
        dc.DrawRectangle(rect)

    def _get_pen(self, dc, event):
        pen = self._get_thin_border_pen(event)
        if self.view_properties.is_highlighted(event):
            if self.view_properties.get_highlight_count(event) % 2 == 0:
                dc.DestroyClippingRegion()
                pen = self._get_thick_border_pen(event)
        return pen

    def _draw_fuzzy_edges(self, dc, rect, event):
        if event.get_fuzzy():
            self._draw_fuzzy_start(dc, rect)
            if not event.get_ends_today():
                self._draw_fuzzy_end(dc, rect)

    def _draw_locked_edges(self, dc, rect, event):
        if event.get_ends_today():
            self._draw_locked_end(dc, rect)
        if event.get_locked():
            self._draw_locked_start(dc, rect)
            self._draw_locked_end(dc, rect)

    def _draw_contents_indicator(self, dc, event, rect):
        if event.has_balloon_data():
            self._draw_balloon_indicator(dc, event, rect)

    def _draw_selection_handles(self, dc, event, rect, selected):
        if not event.locked and selected:
            self._draw_handles(dc, event, rect)

    def _get_thin_border_pen(self, event):
        return self._get_border_pen(event)

    def _get_thick_border_pen(self, event):
        return self._get_border_pen(event, thickness=8)

    def _get_border_pen(self, event, thickness=1):
        return wx.Pen(event.get_border_color(), thickness, wx.PENSTYLE_SOLID)

    def _get_balloon_indicator_brush(self, event):
        base_color = event.get_color()
        darker_color = darken_color(base_color, 0.6)
        brush = wx.Brush(darker_color, wx.BRUSHSTYLE_SOLID)
        return brush

    def _draw_fuzzy_start(self, dc, rect):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_fuzzy_bitmap(), rect.x - 4, rect.y + 4, True)

    def _draw_fuzzy_end(self, dc, rect):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_fuzzy_bitmap(), rect.x + rect.width - 8, rect.y + 4, True)

    def draw_fuzzy(self, dc, event, p1, p2, p3, p4, p5):
        self._erase_outzide_fuzzy_box(dc, p1, p2, p3)
        self._erase_outzide_fuzzy_box(dc, p3, p4, p5)
        self._draw_fuzzy_border(dc, event, p2, p3, p5)

    def _erase_outzide_fuzzy_box(self, dc, p1, p2, p3):
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawPolygon((p1, p2, p3))

    def _draw_fuzzy_border(self, dc, event, p1, p2, p3):
        gc = wx.GraphicsContext.Create(dc)
        path = gc.CreatePath()
        path.MoveToPoint(p1.x, p1.y)
        path.AddLineToPoint(p2.x, p2.y)
        path.AddLineToPoint(p3.x, p3.y)
        gc.SetPen(self._get_thin_border_pen(event))
        gc.StrokePath(path)

    def _draw_locked_start(self, dc, rect):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_lock_bitmap(), rect.x - 7, rect.y + 3, True)

    def _draw_locked_end(self, dc, rect):
        self._inflate_clipping_region(dc, rect)
        dc.DrawBitmap(self._get_lock_bitmap(), rect.x + rect.width - 8, rect.y + 3, True)

    def _draw_progress_box(self, dc, rect, event):
        if event.get_data("progress"):
            self._set_progress_color(dc, event)
            progress_rect = self._get_progress_rect(rect, event)
            dc.DrawRectangle(progress_rect)

    def _set_progress_color(self, dc, event):
        progress_color = event.get_progress_color()
        dc.SetBrush(wx.Brush(wx.Colour(progress_color[0], progress_color[1], progress_color[2])))

    def _get_progress_rect(self, event_rect, event):
        HEIGHT_FACTOR = 0.35
        h = event_rect.height * HEIGHT_FACTOR
        y = event_rect.y + (event_rect.height - h)
        rw, _ = self.scene._calc_width_and_height_for_period_event(event)
        rx = self.scene._calc_x_pos_for_period_event(event)
        w = rw * event.get_data("progress") / 100.0
        return wx.Rect(int(rx), int(y), int(w), int(h))

    def _draw_balloon_indicator(self, dc, event, rect):
        """
        The data contents indicator is a small triangle drawn in the upper
        right corner of the event rectangle.
        """
        corner_x = rect.X + rect.Width
        points = (
            wx.Point(corner_x - DATA_INDICATOR_SIZE, rect.Y),
            wx.Point(corner_x, rect.Y),
            wx.Point(corner_x, rect.Y + DATA_INDICATOR_SIZE),
        )
        dc.SetBrush(self._get_balloon_indicator_brush(event))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawPolygon(points)

    def _draw_text(self, dc, rect, event):
        # Ensure that we can't draw content outside inner rectangle
        if self._there_is_room_for_the_text(rect):
            self._draw_the_text(dc, rect, event)

    def _there_is_room_for_the_text(self, rect):
        return deflate_rect(rect).Width > 0

    def _draw_the_text(self, dc, rect, event):
        self._set_text_foreground_color(dc, event)
        if event.is_container() and EXTENDED_CONTAINER_HEIGHT.enabled():
            EXTENDED_CONTAINER_HEIGHT.draw_container_text_top_adjusted(event.get_text(), dc, rect)
        else:
            self._draw_normal_text(dc, rect, event)
        dc.DestroyClippingRegion()

    def _draw_normal_text(self, dc, rect, event):
        self._set_clipping_rect(dc, rect)
        dc.DrawText(self._get_text(event), self._calc_x_pos(dc, rect, event), self._calc_y_pos(rect))

    def _get_text(self, event):
        if event.get_progress() == 100 and self.view_properties.get_display_checkmark_on_events_done():
            return "\u2714" + event.get_text()
        else:
            return event.get_text()

    def _set_clipping_rect(self, dc, rect):
        dc.SetClippingRegion(deflate_rect(rect))

    def _calc_x_pos(self, dc, rect, event):
        inner_rect = deflate_rect(rect)
        text_x = inner_rect.X
        text_x = self._adjust_x_for_edge_icons(event, rect, text_x)
        text_x = self._adjust_x_for_centered_text(dc, event, inner_rect, text_x)
        return text_x

    def _adjust_x_for_edge_icons(self, event, rect, text_x):
        if event.has_edge_icons():
            text_x += rect.Height // 2
        return text_x

    def _adjust_x_for_centered_text(self, dc, event, inner_rect, text_x):
        if self.center_text:
            text_x = self._center_text(dc, event, inner_rect, text_x)
        return text_x

    def _calc_y_pos(self, rect):
        return deflate_rect(rect).Y

    def _center_text(self, dc, event, inner_rect, text_x):
        width, _ = dc.GetTextExtent(self._get_text(event))
        return max(text_x, text_x + (inner_rect.width - width) // 2)

    def _set_text_foreground_color(self, dc, event):
        try:
            dc.SetTextForeground(get_colour(event.get_category().font_color))
        except AttributeError:
            dc.SetTextForeground(wx.BLACK)

    def _draw_handles(self, dc, event, rect):

        def draw_frame_around_event():
            small_rect = wx.Rect(*rect)
            small_rect.Deflate(1, 1)
            border_color = event.get_border_color()
            border_color = darken_color(border_color)
            pen = wx.Pen(border_color, 1, wx.PENSTYLE_SOLID)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(pen)
            dc.DrawRectangle(small_rect)

        dc.SetClippingRegion(rect)
        draw_frame_around_event()
        self._draw_all_handles(dc, rect, event)
        dc.DestroyClippingRegion()

    def _draw_all_handles(self, dc, rect, event):

        def inflate_clipping_region():
            big_rect = wx.Rect(*rect)
            big_rect.Inflate(HANDLE_SIZE, HANDLE_SIZE)
            dc.DestroyClippingRegion()
            dc.SetClippingRegion(big_rect)

        def set_pen_and_brush():
            dc.SetBrush(wx.BLACK_BRUSH)
            dc.SetPen(wx.BLACK_PEN)

        def create_handle_rect():
            HALF_EVENT_HEIGHT = rect.Height // 2
            y = rect.Y + HALF_EVENT_HEIGHT - HALF_HANDLE_SIZE
            x = rect.X - HALF_HANDLE_SIZE + 1
            return wx.Rect(x, y, HANDLE_SIZE, HANDLE_SIZE)

        def draw_rect(handle_rect, offset):
            handle_rect.Offset(offset, 0)
            dc.DrawRectangle(handle_rect)

        def draw_handle_rects(handle_rect):
            HALF_EVENT_WIDTH = rect.Width // 2
            EVENT_WIDTH = rect.Width
            draw_rect(handle_rect, 0)
            draw_rect(handle_rect, EVENT_WIDTH - 2)
            if not event.ends_today:
                draw_rect(handle_rect, -HALF_EVENT_WIDTH)

        inflate_clipping_region()
        set_pen_and_brush()
        handle_rect = create_handle_rect()
        draw_handle_rects(handle_rect)

    def _draw_hyperlink(self, dc, rect, event):
        if event.get_hyperlink():
            dc.DrawBitmap(self._get_hyperlink_bitmap(), rect.x + rect.width - 14, rect.y + 4, True)

    def _inflate_clipping_region(self, dc, rect):
        copy = wx.Rect(*rect)
        copy.Inflate(10, 0)
        dc.DestroyClippingRegion()
        dc.SetClippingRegion(copy)

    def _get_hyperlink_bitmap(self):
        return self._get_bitmap(self.view_properties.get_hyperlink_icon())

    def _get_lock_bitmap(self):
        return self._get_bitmap(self.view_properties.get_locked_icon())

    def _get_fuzzy_bitmap(self):
        return self._get_bitmap(self.view_properties.get_fuzzy_icon())

    def _get_bitmap(self, name):
        return wx.Bitmap(os.path.join(EVENT_ICONS_DIR, name))

    def _draw_milestone_event(self, dc, rect, event, selected):

        def create_handle_rect():
            HALF_EVENT_HEIGHT = rect.Height // 2
            y = rect.Y + HALF_EVENT_HEIGHT - HALF_HANDLE_SIZE
            x = rect.X - HALF_HANDLE_SIZE + 1
            return wx.Rect(x, y, HANDLE_SIZE, HANDLE_SIZE)

        def draw_shape():
            dc.DestroyClippingRegion()
            dc.SetPen(black_solid_pen(1))
            if event.get_category() is None:
                dc.SetBrush(wx.Brush(wx.Colour(*event.get_default_color()), wx.BRUSHSTYLE_SOLID))
            else:
                dc.SetBrush(wx.Brush(wx.Colour(*event.get_category().get_color()), wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(rect)

        def draw_label():
            x_offset = 6
            y_offset = 2
            try:
                label = event.get_text()[0]
            except IndexError:
                label = " "
            dc.DrawText(label, rect.x + x_offset, rect.y + y_offset)

        def draw_move_handle():
            dc.SetBrush(black_solid_brush())
            handle_rect = create_handle_rect()
            handle_rect.Offset(rect.Width // 2, 0)
            dc.DrawRectangle(handle_rect)

        draw_shape()
        draw_label()
        if selected:
            draw_move_handle()


def deflate_rect(rect, dx=INNER_PADDING, dy=INNER_PADDING):
    return wx.Rect(*rect).Deflate(dx, dy)
