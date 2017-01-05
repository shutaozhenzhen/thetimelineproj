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


import os.path

import wx.calendar

from timelinelib.calendar.gregorian.datepicker.view import NewGregorianDatePicker
from timelinelib.calendar.gregorian.gregorian import Gregorian, GregorianUtils
from timelinelib.calendar.gregorian.timepicker import GregorianTimePicker
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.internaltime import Time
from timelinelib.config.paths import ICONS_DIR


class GregorianDateTimePicker(wx.Panel):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        wx.Panel.__init__(self, parent)
        self.config = config
        self._create_gui()
        self.controller = GregorianDateTimePickerController(
            self.date_picker, self.time_picker, GregorianTimeType().now, on_change)
        self.show_time(show_time)
        self.parent = parent

    def on_return(self):
        try:
            self.parent.on_return()
        except AttributeError:
            pass

    def on_escape(self):
        try:
            self.parent.on_escape()
        except AttributeError:
            pass

    def show_time(self, show=True):
        self.time_picker.Show(show)
        self.GetSizer().Layout()

    def get_value(self):
        try:
            return self.controller.get_value()
        except ValueError:
            pass

    def set_value(self, value):
        self.controller.set_value(value)

    def _create_gui(self):
        self.date_picker = self._create_date_picker()
        image = wx.Bitmap(os.path.join(ICONS_DIR, "calendar.png"))
        self.date_button = wx.BitmapButton(self, bitmap=image)
        self.Bind(wx.EVT_BUTTON, self._date_button_on_click, self.date_button)
        self.time_picker = GregorianTimePicker(self)
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.date_picker, proportion=1,
                  flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.date_button, proportion=0,
                  flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.time_picker, proportion=0,
                  flag=wx.ALIGN_CENTER_VERTICAL)
        self.SetSizerAndFit(sizer)

    def _create_date_picker(self):
        return NewGregorianDatePicker(self, self.config.get_date_formatter())

    def _date_button_on_click(self, evt):
        try:
            wx_date = self.controller.date_tuple_to_wx_date(self.date_picker.GetGregorianDate())
        except ValueError:
            wx_date = wx.DateTime.Now()
        calendar_popup = CalendarPopup(self, wx_date, self.config)
        calendar_popup.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED,
                            self._calendar_on_date_changed)
        calendar_popup.Bind(wx.calendar.EVT_CALENDAR,
                            self._calendar_on_date_changed_dclick)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        calendar_popup.Position(pos, (0, sz[1]))
        calendar_popup.Popup()
        self.calendar_popup = calendar_popup

    def _calendar_on_date_changed(self, evt):
        wx_date = evt.GetEventObject().GetDate()
        date = self.controller.wx_date_to_date_tuple(wx_date)
        self.date_picker.SetGregorianDate(date)

    def _calendar_on_date_changed_dclick(self, evt):
        self.time_picker.SetFocus()
        self.calendar_popup.Dismiss()


class GregorianDateTimePickerController(object):

    def __init__(self, date_picker, time_picker, now_fn, on_change):
        self.date_picker = date_picker
        self.time_picker = time_picker
        self.now_fn = now_fn
        self.on_change = on_change

    def get_value(self):
        if self.time_picker.IsShown():
            hour, minute, second = self.time_picker.GetGregorianTime()
        else:
            hour, minute, second = (0, 0, 0)
        year, month, day = self.date_picker.GetGregorianDate()
        return Gregorian(year, month, day, hour, minute, second).to_time()

    def set_value(self, time):
        if time is None:
            time = self.now_fn()
        self.date_picker.SetGregorianDate(GregorianUtils.from_time(time).to_date_tuple())
        self.time_picker.SetGregorianTime(GregorianUtils.from_time(time).to_time_tuple())
        if self.on_change is not None:
            self.on_change()

    def date_tuple_to_wx_date(self, date):
        year, month, day = date
        return wx.DateTimeFromDMY(day, month - 1, year, 0, 0, 0)

    def wx_date_to_date_tuple(self, wx_date):
        return (wx_date.Year, wx_date.Month + 1, wx_date.Day)


class CalendarPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wx_date, config):
        self.config = config
        wx.PopupTransientWindow.__init__(self, parent, style=wx.BORDER_NONE)
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
        cal = wx.calendar.CalendarCtrl(self, -1, wx_date,
                                       pos=(border, border), style=style)
        self._set_cal_range(cal)
        return cal

    def _get_cal_style(self):
        style = (wx.calendar.CAL_SHOW_HOLIDAYS |
                 wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
        if self.config.get_week_start() == "monday":
            style |= wx.calendar.CAL_MONDAY_FIRST
        else:
            style |= wx.calendar.CAL_SUNDAY_FIRST
        return style

    def _set_cal_range(self, cal):
        min_date, _ = GregorianTimeType().get_min_time()
        max_date, _ = GregorianTimeType().get_max_time()
        min_date = self.time_to_wx_date(min_date)
        max_date = self.time_to_wx_date(max_date) - wx.DateSpan.Day()
        cal.SetDateRange(min_date, max_date)

    def time_to_wx_date(self, time):
        year, month, day = GregorianUtils.from_time(time).to_date_tuple()
        try:
            return wx.DateTimeFromDMY(day, month - 1, year, 0, 0, 0)
        except OverflowError:
            if year < 0:
                year, month, day = GregorianUtils.from_time(Time(0, 0)).to_date_tuple()
                return wx.DateTimeFromDMY(day, month - 1, year, 0, 0, 0)

    def _bind_events(self):
        def on_month(evt):
            self.controller.on_month()

        def on_day(evt):
            self.controller.on_day()

        self.cal.Bind(wx.calendar.EVT_CALENDAR_MONTH, on_month)
        self.cal.Bind(wx.calendar.EVT_CALENDAR_DAY, on_day)

    def OnDismiss(self):
        self.controller.on_dismiss()


class CalendarPopupController(object):

    def __init__(self, calendar_popup):
        self.calendar_popup = calendar_popup
        self.repop = False
        self.repoped = False

    def on_month(self):
        self.repop = True

    def on_day(self):
        self.repop = True

    def on_dismiss(self):
        # This funny code makes the calender control stay open when you change
        # month or day. The control is closed on a double-click on a day or
        # a single click outside of the control
        if self.repop and not self.repoped:
            self.calendar_popup.Popup()
            self.repoped = True