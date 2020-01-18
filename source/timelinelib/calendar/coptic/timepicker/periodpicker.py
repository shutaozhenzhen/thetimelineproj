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


from timelinelib.calendar.coptic.timetype.timetype import CopticTimeType
from timelinelib.wxgui.framework import Panel
from timelinelib.calendar.coptic.timepicker.periodpickercontroller import CopticPeriodPickerController


class CopticPeriodPicker(Panel):

    """
    <BoxSizerVertical>
        <BoxSizerHorizontal>
            <TimePicker
                name="start_time"
                time_type="$(time_type)"
                config="$(config)"
            />
            <Spacer />
            <StaticText
                label="$(to_label)"
                name="to_label"
                align="ALIGN_CENTER_VERTICAL"
            />
            <Spacer />
            <TimePicker
                name="end_time"
                time_type="$(time_type)"
                config="$(config)"
            />
        </BoxSizerHorizontal>
        <Spacer />
        <BoxSizerHorizontal>
            <CheckBox
                name="period_checkbox"
                event_EVT_CHECKBOX="on_period_checkbox_changed"
                label="$(period_checkbox_text)" />
            <CheckBox
                name="show_time_checkbox"
                event_EVT_CHECKBOX="on_show_time_checkbox_changed"
                label="$(show_time_checkbox_text)"
            />
        </BoxSizerHorizontal>
    </BoxSizerVertical>
    """

    def __init__(self, parent, config, name=None):
        Panel.__init__(self, CopticPeriodPickerController, parent, {
            "time_type": CopticTimeType(),
            "config": config,
            "to_label": _("to"),
            "period_checkbox_text": _("Period"),
            "show_time_checkbox_text": _("Show time"),
        })

    def GetValue(self):
        return self.controller.get_value()

    def SetValue(self, time_period):
        self.controller.set_value(time_period)

    def GetStartValue(self):
        return self.start_time.get_value()

    def SetStartValue(self, time):
        self.start_time.set_value(time)

    def GetEndValue(self):
        return self.end_time.get_value()

    def SetEndValue(self, time):
        self.end_time.set_value(time)

    def GetShowPeriod(self):
        return self.period_checkbox.GetValue()

    def SetShowPeriod(self, show):
        self.period_checkbox.SetValue(show)
        self.to_label.Show(show)
        self.end_time.Show(show)
        self.Layout()

    def GetShowTime(self):
        return self.show_time_checkbox.GetValue()

    def SetShowTime(self, show):
        self.show_time_checkbox.SetValue(show)
        self.start_time.show_time(show)
        self.end_time.show_time(show)
        self.Layout()

    def DisableTime(self):
        self.SetShowTime(False)
        self.show_time_checkbox.Disable()
