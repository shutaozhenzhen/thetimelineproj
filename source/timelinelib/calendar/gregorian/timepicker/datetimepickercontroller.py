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

from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.wxgui.utils import display_information_message


ERROR_MESSAGE = _("The date control can't handle the given date")


class GregorianDateTimePickerController:

    def __init__(self, view, date_picker, time_picker, now_fn, on_change):
        self._view = view
        self.date_picker = date_picker
        self.time_picker = time_picker
        self.now_fn = now_fn
        self.on_change = on_change

    def get_value(self):
        if self.time_picker.IsShown():
            hour, minute, second = self.time_picker.GetGregorianTime()
        else:
            hour, minute, second = (0, 0, 0)
        year, month, day = self.date_picker.GetDate()
        return GregorianDateTime(year, month, day, hour, minute, second).to_time()

    def set_value(self, time):
        if time is None:
            time = self.now_fn()
        self.date_picker.SetDate(GregorianDateTime.from_time(time).to_date_tuple())
        self.time_picker.SetGregorianTime(GregorianDateTime.from_time(time).to_time_tuple())
        self.changed()

    def changed(self):
        if self.on_change is not None:
            self.on_change()

    def date_tuple_to_wx_date(self, date):
        year, month, day = date
        return wx.DateTime.FromDMY(day, month - 1, year, 0, 0, 0)

    def wx_date_to_date_tuple(self, wx_date):
        return (wx_date.year, wx_date.month + 1, wx_date.day)

    def date_button_on_click(self, evt):
        try:
            dt = self.date_picker.GetDate()
            wx_date = self.date_tuple_to_wx_date(dt)
        except ValueError:
            wx_date = wx.DateTime.Now()
        except wx._core.PyAssertionError:
            display_information_message('wx.DateTime limitation', ERROR_MESSAGE)
        else:
            try:
                self._view.PopupCalendar(evt, wx_date)
            except wx._core.PyAssertionError:
                display_information_message('GUI control limitation', ERROR_MESSAGE)
