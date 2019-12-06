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

from timelinelib.calendar.coptic.coptic import CopticDateTime
from timelinelib.calendar.coptic.time import CopticDelta
from timelinelib.calendar.coptic.timepicker.datecontroller import CopticDatePickerController
from timelinelib.calendar.coptic.timetype.timetype import CopticTimeType
from timelinelib.wxgui.components.textctrl import TextCtrl


class CopticDatePicker(wx.Panel):

    def __init__(self, parent, date_formatter, name=None):
        wx.Panel.__init__(self, parent)
        self._controller = CopticDatePickerController(self)
        self._create_gui(date_formatter)
        self._controller.on_init(
            date_formatter,
            DateModifier()
        )

    def _create_gui(self, date_formatter):
        self._create_date_text(date_formatter)
        self._create_bc_button()
        self._layout()

    def _create_date_text(self, date_formatter):
        self.date_text = TextCtrl(
            self,
            style=wx.TE_PROCESS_ENTER,
            fit_text=self._format_sample_date(date_formatter)
        )
        self.date_text.Bind(wx.EVT_CHAR, self._controller.on_char)
        self.date_text.Bind(wx.EVT_TEXT, self._controller.on_text)

    def _create_bc_button(self):
        label = _("BC")
        self.bc_button = wx.ToggleButton(self, label=label)
        label_width = self.bc_button.GetTextExtent(label)[0]
        self.bc_button.SetMinSize((label_width + 20, -1))

    def _layout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.date_text, flag=wx.EXPAND, proportion=1)
        sizer.Add(self.bc_button, flag=wx.EXPAND)
        self.SetSizer(sizer)

    def _format_sample_date(self, date_formatter):
        return date_formatter.format(
            CopticDateTime.from_time(
                CopticTimeType().now()
            ).to_date_tuple()
        )[0]

    def GetCopticDate(self):
        return self._controller.get_coptic_date()

    def SetCopticDate(self, date):
        self._controller.set_coptic_date(date)

    def GetText(self):
        return self.date_text.GetValue()

    def SetText(self, text):
        x = self.date_text.GetInsertionPoint()
        self.date_text.SetValue(text)
        self.date_text.SetInsertionPoint(x)

    def SetSelection(self, pos_lenght_tuple):
        (pos, lenght) = pos_lenght_tuple
        self.date_text.SetSelection(pos, pos + lenght)

    def GetCursorPosition(self):
        return self.date_text.GetInsertionPoint()

    def GetIsBc(self):
        return self.bc_button.GetValue()

    def SetIsBc(self, is_bc):
        self.bc_button.SetValue(is_bc)

    def SetBackgroundColour(self, colour):
        self.date_text.SetBackgroundColour(colour)
        self.date_text.Refresh()


class DateModifier:

    def increment_year(self, date):
        max_year = CopticDateTime.from_time(CopticTimeType().get_max_time()).year
        year, month, day = date
        if year < max_year - 1:
            return self._set_valid_day(year + 1, month, day)
        return date

    def increment_month(self, date):
        max_year = CopticDateTime.from_time(CopticTimeType().get_max_time()).year
        year, month, day = date
        if month < 13:
            return self._set_valid_day(year, month + 1, day)
        elif year < max_year - 1:
            return self._set_valid_day(year + 1, 1, day)
        return date

    def increment_day(self, date):
        year, month, day = date
        time = CopticDateTime.from_ymd(year, month, day).to_time()
        if time < CopticTimeType().get_max_time() - CopticDelta.from_days(1):
            return CopticDateTime.from_time(time + CopticDelta.from_days(1)).to_date_tuple()
        return date

    def decrement_year(self, date):
        year, month, day = date
        if year > CopticDateTime.from_time(CopticTimeType().get_min_time()).year:
            return self._set_valid_day(year - 1, month, day)
        return date

    def decrement_month(self, date):
        year, month, day = date
        if month > 1:
            return self._set_valid_day(year, month - 1, day)
        elif year > CopticDateTime.from_time(CopticTimeType().get_min_time()).year:
            return self._set_valid_day(year - 1, 13, day)
        return date

    def decrement_day(self, date):
        year, month, day = date
        if day > 1:
            return self._set_valid_day(year, month, day - 1)
        elif month > 1:
            return self._set_valid_day(year, month - 1, 30)
        elif year > CopticDateTime.from_time(CopticTimeType().get_min_time()).year:
            return self._set_valid_day(year - 1, 12, 30)
        return date

    def _set_valid_day(self, new_year, new_month, new_day):
        done = False
        while not done:
            try:
                date = CopticDateTime.from_ymd(new_year, new_month, new_day)
                done = True
            except Exception:
                new_day -= 1
        return date.to_date_tuple()
