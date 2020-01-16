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

from timelinelib.calendar.coptic.timepicker.datepicker import CopticDatePicker
from timelinelib.calendar.coptic.timepicker.timepciker import CopticTimePicker
from timelinelib.calendar.coptic.timetype.timetype import CopticTimeType
from timelinelib.calendar.coptic.timepicker.calendarpopup import CalendarPopup
from timelinelib.calendar.coptic.timepicker.datetimepickercontoller import CopticDateTimePickerController
from timelinelib.config.paths import ICONS_DIR


class CopticDateTimePicker(wx.Panel):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        print('CopticDateTimePicker', on_change)
        wx.Panel.__init__(self, parent)
        self.config = config
        self._on_change = on_change
        self.calendar_popup = None
        self._create_gui()
        self.controller = CopticDateTimePickerController(self, self.date_picker, self.time_picker,
                                                         CopticTimeType().now, on_change)
        self.show_time(show_time)
        self.parent = parent

    def PopupCalendar(self, evt, wx_date):
        calendar_popup = CalendarPopup(self, wx_date, self.config)
        calendar_popup.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self._calendar_on_date_changed)
        calendar_popup.Bind(wx.adv.EVT_CALENDAR, self._calendar_on_date_changed_dclick)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        calendar_popup.Position(pos, (0, sz[1]))
        calendar_popup.Popup()
        self.calendar_popup = calendar_popup

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
        self.time_picker = CopticTimePicker(self)
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.date_picker, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.date_button, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.time_picker, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        self.SetSizerAndFit(sizer)

    def _create_date_picker(self):
        return CopticDatePicker(self, self.config.get_date_formatter(), on_change=self._on_change)

    def _date_button_on_click(self, evt):
        self.controller.date_button_on_click(evt)

    @staticmethod
    def _out_of_date_range(wx_date):
        """It's is a limitation in the wx.adv.CalendarCtrl class
        that has this date limit."""
        return str(wx_date) < '1601-01-01 00:00:00'

    def _calendar_on_date_changed(self, evt):
        wx_date = evt.GetEventObject().GetDate()
        date = self.controller.wx_date_to_date_tuple(wx_date)
        self.date_picker.SetCopticDate(date)
        self.controller.changed()

    def _calendar_on_date_changed_dclick(self, evt):
        self.time_picker.SetFocus()
        self.calendar_popup.Dismiss()
        self.controller.changed()
