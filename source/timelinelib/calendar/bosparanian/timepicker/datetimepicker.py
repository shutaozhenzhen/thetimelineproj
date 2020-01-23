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

from timelinelib.calendar.bosparanian.timetype.timetype import BosparanianTimeType
from timelinelib.calendar.bosparanian.timepicker.datepicker import BosparanianDatePicker
from timelinelib.calendar.generic.timepicker.timepicker import TimePicker
from timelinelib.calendar.bosparanian.bosparanian import is_valid_time
from timelinelib.calendar.bosparanian.bosparanian import BosparanianDateTime
from timelinelib.calendar.generic.timepicker.datetimepickercontroller import DateTimePickerController


class BosparanianDateTimePicker(wx.Panel):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        wx.Panel.__init__(self, parent)
        self.config = config
        self._create_gui(on_change)
        self.controller = DateTimePickerController(self, BosparanianDateTime,
                                                   self.date_picker, self.time_picker,
                                                   BosparanianTimeType().now, on_change=on_change)
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

    def _create_gui(self, on_change):
        self.date_picker = BosparanianDatePicker(self, on_change)
        self.time_picker = TimePicker(self, False, [':'], is_valid_time)
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.date_picker, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.time_picker, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        self.SetSizerAndFit(sizer)
