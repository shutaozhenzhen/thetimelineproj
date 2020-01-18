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


import os.path

import wx.adv

from timelinelib.calendar.gregorian.timepicker.datepicker import GregorianDatePicker
from timelinelib.calendar.gregorian.timepicker.timepicker import GregorianTimePicker
from timelinelib.calendar.generic.timepicker.calendarpopup import CalendarPopup
from timelinelib.calendar.gregorian.timepicker.datetimepickercontroller import GregorianDateTimePickerController
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.config.paths import ICONS_DIR


class GregorianDateTimePicker(wx.Panel):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        wx.Panel.__init__(self, parent)
        self._parent = parent
        self._config = config
        self._calendar_popup = None
        self._time_type = GregorianTimeType()
        self._date_picker = GregorianDatePicker(self, self._config.get_date_formatter(), on_change=on_change)
        self._time_picker = GregorianTimePicker(self, self._config)
        self._create_gui()
        self._controller = GregorianDateTimePickerController(self, self._date_picker, self._time_picker,
                                                             GregorianTimeType().now, on_change)
        self.show_time(show_time)

    def PopupCalendar(self, evt, wx_date):
        calendar_popup = CalendarPopup(self, wx_date, self._config, self._time_type)
        calendar_popup.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self._calendar_on_date_changed)
        calendar_popup.Bind(wx.adv.EVT_CALENDAR, self._calendar_on_date_changed_dclick)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        calendar_popup.Position(pos, (0, sz[1]))
        calendar_popup.Popup()
        self._calendar_popup = calendar_popup

    def on_return(self):
        try:
            self._parent.on_return()
        except AttributeError:
            pass

    def on_escape(self):
        try:
            self._parent.on_escape()
        except AttributeError:
            pass

    def show_time(self, show=True):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        if show:
            sizer.Add(self._date_picker, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self.date_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self._time_picker, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
            self._time_picker.Show()
        else:
            sizer.Add(self._date_picker, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(self.date_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
            self._time_picker.Hide()
        self.SetSizerAndFit(sizer)

    def get_value(self):
        try:
            return self._controller.get_value()
        except ValueError:
            pass

    def set_value(self, value):
        self._controller.set_value(value)

    def _create_gui(self):
        image = wx.Bitmap(os.path.join(ICONS_DIR, "calendar.png"))
        self.date_button = wx.BitmapButton(self, bitmap=image)
        self.Bind(wx.EVT_BUTTON, self._date_button_on_click, self.date_button)
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._date_picker, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.date_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self._time_picker, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        self.SetSizerAndFit(sizer)

    def _date_button_on_click(self, evt):
        self._controller.date_button_on_click(evt)

    @staticmethod
    def _out_of_date_range(wx_date):
        """It's is a limitation in the wx.adv.CalendarCtrl class
        that has this date limit."""
        return str(wx_date) < '1601-01-01 00:00:00'

    def _calendar_on_date_changed(self, evt):
        wx_date = evt.GetEventObject().GetDate()
        date = self._controller.wx_date_to_date_tuple(wx_date)
        self._date_picker.SetDate(date)
        self._controller.changed()

    def _calendar_on_date_changed_dclick(self, evt):
        self._time_picker.SetFocus()
        self._calendar_popup.Dismiss()
        self._controller.changed()
