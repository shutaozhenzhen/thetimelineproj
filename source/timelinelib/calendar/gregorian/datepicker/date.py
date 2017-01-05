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

from timelinelib.calendar.gregorian.datepicker.controller import NewGregorianDatePickerController


class GregorianDatePicker(wx.Panel):

    def __init__(self, parent, date_formatter, name=None):
        wx.Panel.__init__(self, parent)
        self.controller = NewGregorianDatePickerController(self)
        self._create_gui()
        self.controller.on_init(
            date_formatter,
            DateModifier()
        )

    def _create_gui(self):
        self._create_date_text()
        self._create_bc_button()
        self._layout()

    def _create_date_text(self):
        self.date_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.date_text.Bind(wx.EVT_CHAR, self.controller.on_char)
        self.date_text.Bind(wx.EVT_TEXT, self.controller.on_text)

    def _create_bc_button(self):
        label = _("BC")
        self.bc_button = wx.ToggleButton(self, label=label)
        (label_width, label_height) = self.bc_button.GetTextExtent(label)
        self.bc_button.SetMinSize((label_width + 20, -1))

    def _layout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.date_text, flag=wx.EXPAND, proportion=1)
        sizer.Add(self.bc_button, flag=wx.EXPAND)
        self.SetSizer(sizer)

    def GetGregorianDate(self):
        return self.controller.get_gregorian_date()

    def SetGregorianDate(self, date):
        self.controller.set_gregorian_date(date)

    def GetText(self):
        return self.date_text.GetValue()

    def SetText(self, text):
        x = self.date_text.GetInsertionPoint()
        self.date_text.SetValue(text)
        self.date_text.SetInsertionPoint(x)

    def SetSelection(self, pos_lenght_tuple):
        (pos, lenght) = pos_lenght_tuple
        self.date_text.SetSelection(pos, pos+lenght)

    def GetCursorPosition(self):
        return self.date_text.GetInsertionPoint()

    def GetIsBc(self):
        return self.bc_button.GetValue()

    def SetIsBc(self, is_bc):
        self.bc_button.SetValue(is_bc)

    def SetBackgroundColour(self, colour):
        self.date_text.SetBackgroundColour(colour)
        self.date_text.Refresh()


class DateModifier(object):

    def __init__(self):
        import timelinelib.calendar.gregorian.datepicker.utils as gdp
        self.gdp = gdp

    def increment_year(self, date):
        return self.gdp.increment_year(date)

    def increment_month(self, date):
        return self.gdp.increment_month(date)

    def increment_day(self, date):
        return self.gdp.increment_day(date)

    def decrement_year(self, date):
        return self.gdp.decrement_year(date)

    def decrement_month(self, date):
        return self.gdp.decrement_month(date)

    def decrement_day(self, date):
        return self.gdp.decrement_day(date)
