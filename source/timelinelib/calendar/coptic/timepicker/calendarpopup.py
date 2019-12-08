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


import wx.adv

from timelinelib.calendar.coptic.coptic import CopticDateTime
from timelinelib.calendar.coptic.time import CopticTime
from timelinelib.calendar.coptic.timepicker.calendarpopupcontroller import CalendarPopupController
from timelinelib.calendar.coptic.timetype.timetype import CopticTimeType


class CalendarPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wx_date, config):
        self.config = config
        wx.PopupTransientWindow.__init__(self, parent, flags=wx.BORDER_NONE)
        self._create_gui(wx_date)
        self.controller = CalendarPopupController(self)
        self._bind_events()

    def _create_gui(self, wx_date):
        BORDER = 2
        self.cal = self._create_calendar_control(wx_date, BORDER)
        size = self.cal.GetBestSize()
        self.SetSize((size.width + BORDER * 2, size.height + BORDER * 2))

    def _create_calendar_control(self, wx_date, border):
        style = self._get_cal_style()
        cal = wx.adv.CalendarCtrl(self, -1, wx_date, pos=(border, border), style=style)
        self._set_cal_range(cal)
        return cal

    def _get_cal_style(self):
        style = (wx.adv.CAL_SHOW_HOLIDAYS |
                 wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        if self.config.get_week_start() == "monday":
            style |= wx.adv.CAL_MONDAY_FIRST
        else:
            style |= wx.adv.CAL_SUNDAY_FIRST
        return style

    def _set_cal_range(self, cal):
        min_date = CopticTimeType().get_min_time()
        max_date = CopticTimeType().get_max_time()
        min_date = self.time_to_wx_date(min_date)
        max_date = self.time_to_wx_date(max_date) - wx.DateSpan.Day()
        cal.SetDateRange(min_date, max_date)

    @staticmethod
    def time_to_wx_date(time):
        year, month, day = CopticDateTime.from_time(time).to_date_tuple()
        try:
            return wx.DateTime.FromDMY(day, month - 1, year, 0, 0, 0)
        except OverflowError:
            if year < 0:
                year, month, day = CopticDateTime.from_time(CopticTime(0, 0)).to_date_tuple()
                return wx.DateTime.FromDMY(day, month - 1, year, 0, 0, 0)

    def _bind_events(self):
        def on_month(evt):
            self.controller.on_month()

        def on_day(evt):
            self.controller.on_day()

        self.cal.Bind(wx.adv.EVT_CALENDAR_MONTH, on_month)
        self.cal.Bind(wx.adv.EVT_CALENDAR_DAY, on_day)

    def OnDismiss(self):
        self.controller.on_dismiss()
