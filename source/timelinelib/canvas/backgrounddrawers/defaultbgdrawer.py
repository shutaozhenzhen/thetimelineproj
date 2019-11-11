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


import wx


class DefaultBackgroundDrawer:

    OFFSET = 15

    def __init__(self):
        self._drawer = None

    def draw(self, drawer, dc, scene, timeline, colorize_weekends, weekend_colour, bg_colour):
        self._drawer = drawer
        erase_dc_background(dc, bg_colour)
        self._draw_eras(dc, timeline)
        self._draw_weekend_days(dc, scene, colorize_weekends, weekend_colour)

    def _draw_weekend_days(self, dc, scene, colorize_weekends, weekend_colour):
        if colorize_weekends and scene.minor_strip_is_day():
            _, h = dc.GetSize()
            for strip_period in scene.minor_strip_data:
                if scene.is_weekend_day(strip_period.start_time):
                    self._draw_weekend_rect(strip_period, h, weekend_colour)

    def _draw_eras(self, dc, timeline):
        _, h = dc.GetSize()
        for era in timeline.get_all_periods():
            if self._drawer.period_is_visible(era.get_time_period()):
                self._draw_era(era, h)

    def _draw_era(self, era, h):
        self._draw_era_rect(era, h)
        self._draw_era_name_in_center_of_visible_era(era, h)

    def _draw_era_rect(self, era, h):
        self._draw_timeperiod_rect(era.get_time_period(), h, era.get_color())

    def _draw_weekend_rect(self, timeperiod, h, weekend_colour):
        self._draw_timeperiod_rect(timeperiod, h, weekend_colour, self.OFFSET)

    def _draw_timeperiod_rect(self, timeperiod, h, colour, offset=0):
        x, width = self._get_timeperiod_measures(timeperiod)
        self._draw_backgound_rect(x, h, max(1, width), colour, offset)

    def _draw_backgound_rect(self, x, h, width, colour, offset):
        set_dc_color(self._drawer.dc, colour)
        self._drawer.dc.DrawRectangle(x, offset, width, h - 2 * offset)

    def _draw_era_name_in_center_of_visible_era(self, era, h):
        x, width = self._get_timeperiod_measures(era.get_time_period())
        wt, ht = self._drawer.dc.GetTextExtent(era.get_name())
        self._drawer.dc.DrawText(era.get_name(), x + width // 2 - wt // 2, h - ht)

    def _get_timeperiod_measures(self, time_period):
        x1, x2 = self._drawer.get_period_xpos(time_period)
        return x1, x2 - x1


def erase_dc_background(dc, bg_colour):
    w, h = dc.GetSize()
    set_dc_color(dc, bg_colour)
    dc.DrawRectangle(0, 0, w, h)


def set_dc_color(dc, color):
    dc.SetPen(wx.Pen(color))
    dc.SetBrush(wx.Brush(color))
