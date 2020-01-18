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

from timelinelib.calendar.generic.timepicker.calendarpopupcontroller import CalendarPopupController


class CalendarPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wx_date, config, time_type):
        self._parent = parent
        self.config = config
        wx.PopupTransientWindow.__init__(self, parent, flags=wx.BORDER_NONE)
        self._create_gui(config, wx_date, time_type)
        self.controller = CalendarPopupController(self)

    def SelectionChanged(self):
        wx.PostEvent(self, wx.adv.CalendarEvent(self.cal, self.cal.GetDate(), wx.adv.EVT_CALENDAR_SEL_CHANGED.typeId))

    def _create_gui(self, config, wx_date, time_type):
        BORDER = 2
        position = (BORDER, BORDER)
        style = self._get_cal_style(config)
        min_date = time_type.get_min_wx_time()
        max_date = time_type.get_max_wx_time()
        self.cal = wx.adv.CalendarCtrl(self, -1, wx_date, pos=position, style=style)
        self.cal.SetDateRange(min_date, max_date)
        size = self.cal.GetBestSize()
        self.SetSize((size.width + BORDER * 2, size.height + BORDER * 2))

    @staticmethod
    def _get_cal_style(config):
        style = (wx.adv.CAL_SHOW_HOLIDAYS | wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        if config.get_week_start() == "monday":
            style |= wx.adv.CAL_MONDAY_FIRST
        else:
            style |= wx.adv.CAL_SUNDAY_FIRST
        return style

    def OnDismiss(self):
        self.controller.on_dismiss()
