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


import wx

from timelinelib.wxgui.components.timepickerwrapper.controller import TimePickerWrapperController


class TimePickerWrapper(wx.Panel):

    @staticmethod
    def create(time_type, time_picker_class):
        def init_wrapper(parent, **kwargs):
            return TimePickerWrapper(
                parent, time_type, time_picker_class, **kwargs
            )
        return init_wrapper

    def __init__(self, parent, time_type, time_picker_class, **kwargs):
        wx.Panel.__init__(self, parent)
        self._create_gui(time_picker_class, **kwargs)
        self._controller = TimePickerWrapperController(self)
        self._controller.on_init(time_type, self._time_picker)

    def set_value(self, value):
        self._controller.set_value(value)

    def get_value(self):
        return self._controller.get_value()

    def show_time(self, show):
        self._controller.show_time(show)

    def ShowTimePicker(self):
        self._time_picker.Show()
        self._out_of_range_button.Hide()
        self.SetSizerAndFit(self.GetSizer())

    def ShowOutOfRangeControl(self):
        self._time_picker.Hide()
        self._out_of_range_button.Show()

    def _create_gui(self, time_picker_class, **kwargs):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(
            self._create_time_picker(time_picker_class, **kwargs)
        )
        sizer.Add(
            self._create_out_of_range_control(),
            flag=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL
        )
        self.SetSizerAndFit(sizer)

    def _create_time_picker(self, time_picker_class, **kwargs):
        self._time_picker = time_picker_class(self, **kwargs)
        return self._time_picker

    def _create_out_of_range_control(self):
        self._out_of_range_button = wx.Button(self, label=_("Unable to edit"))
        self._out_of_range_button.Bind(wx.EVT_BUTTON, self._on_out_of_range_click)
        return self._out_of_range_button

    def _on_out_of_range_click(self, event):
        from timelinelib.wxgui.utils import display_information_message
        caption = _("Unable to edit")
        message = _("The given time can't be edited with this control.\n\nThis is likely because the time is outside the current calendar range.")
        display_information_message(caption, message, parent=self)
