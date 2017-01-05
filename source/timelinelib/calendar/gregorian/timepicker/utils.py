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

from timelinelib.calendar.gregorian.gregorian import Gregorian, GregorianUtils
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.internaltime import delta_from_days
from timelinelib.wxgui.components import TextPatternControl


YEAR_INDEX = 0
MONTH_INDEX = 1
DAY_INDEX = 2


class GregorianDatePicker(wx.Panel):

    def __init__(self, parent, gregorian_date_formatter):
        wx.Panel.__init__(self, parent)
        self._gregorian_date_formatter = gregorian_date_formatter
        self._create_date_text()
        self._create_bc_button()
        self._layout()

    def _create_date_text(self):
        self.date_text = TextPatternControl(self)
        self.date_text.SetSeparators([self._get_separator(), self._get_separator()])
        self.date_text.SetValidator(self._is_date_valid)
        self.date_text.SetUpHandler(self._get_year_group(), self._increment_year)
        self.date_text.SetUpHandler(self._get_month_group(), self._increment_month)
        self.date_text.SetUpHandler(self._get_day_group(), self._increment_day)
        self.date_text.SetDownHandler(self._get_year_group(), self._decrement_year)
        self.date_text.SetDownHandler(self._get_month_group(), self._decrement_month)
        self.date_text.SetDownHandler(self._get_day_group(), self._decrement_day)
        (date_width, date_height) = self.date_text.GetTextExtent("0000%s00%s00" % (
            self._get_separator(),
            self._get_separator()
        ))
        self.date_text.SetMinSize((date_width + 20, -1))

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
        return parts_to_gregorian_date(
            self._get_regions(),
            self.date_text.GetParts(),
            self.bc_button.GetValue()
        )

    def SetGregorianDate(self, date):
        (text_parts, is_bc) = gregorian_date_to_parts(self._get_regions(), date)
        self.date_text.SetParts(text_parts)
        self.bc_button.SetValue(is_bc)
        def click(event):
            self.date_text.Validate()
        self.bc_button.Bind(wx.EVT_TOGGLEBUTTON, click)

    def _is_date_valid(self):
        try:
            self.GetGregorianDate()
        except ValueError:
            return False
        else:
            return True

    def _increment_year(self):
        self.SetGregorianDate(increment_year(self.GetGregorianDate()))

    def _increment_month(self):
        self.SetGregorianDate(increment_month(self.GetGregorianDate()))

    def _increment_day(self):
        self.SetGregorianDate(increment_day(self.GetGregorianDate()))

    def _decrement_year(self):
        self.SetGregorianDate(decrement_year(self.GetGregorianDate()))

    def _decrement_month(self):
        self.SetGregorianDate(decrement_month(self.GetGregorianDate()))

    def _decrement_day(self):
        self.SetGregorianDate(decrement_day(self.GetGregorianDate()))

    def _get_separator(self):
        return self._gregorian_date_formatter.separator()

    def _get_regions(self):
        return self._gregorian_date_formatter.get_regions()

    def _get_year_group(self):
        return self._gregorian_date_formatter.get_regions().index(YEAR_INDEX)

    def _get_month_group(self):
        return self._gregorian_date_formatter.get_regions().index(MONTH_INDEX)

    def _get_day_group(self):
        return self._gregorian_date_formatter.get_regions().index(DAY_INDEX)


def parts_to_gregorian_date(regions, parts, is_bc):
    values = {}
    for (region, value) in zip(regions, parts):
        values[region] = int(value)
    year = values[YEAR_INDEX]
    month = values[MONTH_INDEX]
    day = values[DAY_INDEX]
    if is_bc:
        year = 1-year
    time = Gregorian(year, month, day, 0, 0, 0).to_time()
    if (time >= GregorianTimeType().get_max_time()[0] or
        time < GregorianTimeType().get_min_time()[0]):
        raise ValueError()
    return (year, month, day)


def gregorian_date_to_parts(regions, date):
    parts = []
    is_bc = False
    for region in regions:
        if region == YEAR_INDEX:
            year = date[region]
            if year <= 0:
                year = 1 - year
                is_bc = True
            parts.append("%04d" % year)
        else:
            parts.append("%02d" % date[region])
    return (parts, is_bc)


def increment_year(date):
    max_year = GregorianUtils.from_time(GregorianTimeType().get_max_time()[0]).year
    year, month, day = date
    if year < max_year - 1:
        return _set_valid_day(year + 1, month, day)
    return date


def increment_month(date):
    max_year = GregorianUtils.from_time(GregorianTimeType().get_max_time()[0]).year
    year, month, day = date
    if month < 12:
        return _set_valid_day(year, month + 1, day)
    elif year < max_year - 1:
        return _set_valid_day(year + 1, 1, day)
    return date


def increment_day(date):
    year, month, day = date
    time = GregorianUtils.from_date(year, month, day).to_time()
    if time <  GregorianTimeType().get_max_time()[0] - delta_from_days(1):
        return GregorianUtils.from_time(time + delta_from_days(1)).to_date_tuple()
    return date


def decrement_year(date):
    year, month, day = date
    if year > GregorianUtils.from_time(GregorianTimeType().get_min_time()[0]).year:
        return _set_valid_day(year - 1, month, day)
    return date


def decrement_month(date):
    year, month, day = date
    if month > 1:
        return _set_valid_day(year, month - 1, day)
    elif year > GregorianUtils.from_time(GregorianTimeType().get_min_time()[0]).year:
        return _set_valid_day(year - 1, 12, day)
    return date


def decrement_day(date):
    year, month, day = date
    if day > 1:
        return _set_valid_day(year, month, day - 1)
    elif month > 1:
        return _set_valid_day(year, month - 1, 31)
    elif year > GregorianUtils.from_time(GregorianTimeType().get_min_time()[0]).year:
        return _set_valid_day(year - 1, 12, 31)
    return date


def _set_valid_day(new_year, new_month, new_day):
    done = False
    while not done:
        try:
            date = GregorianUtils.from_date(new_year, new_month, new_day)
            done = True
        except Exception:
            new_day -= 1
    return date.to_date_tuple()
