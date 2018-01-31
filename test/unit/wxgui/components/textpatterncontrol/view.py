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


import datetime

import humblewx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.framework import Dialog


class describe_text_pattern_control_view(UnitTestCase):

    def test_show_manual_test_dialog(self):
        self.show_dialog(TextPatternControlManualTestDialog)


class TextPatternControlManualTestDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="1" border="ALL">
            <Button label="before" />
            <TextPatternControl name="date" />
            <Button label="after" />
        </FlexGridSizer>
    </BoxSizerVertical>
    """

    YEAR_GROUP = 0
    MONTH_GROUP = 1
    DAY_GROUP = 2

    def __init__(self):
        Dialog.__init__(self, humblewx.Controller, None, {
        })
        self.date.SetSeparators(["-", "-"])
        self.date.SetParts(["2015", "12", "05"])
        self.date.SetValidator(self._is_date_valid)
        self.date.SetUpHandler(self.YEAR_GROUP, self._increment_year)
        self.date.SetUpHandler(self.MONTH_GROUP, self._increment_month)
        self.date.SetUpHandler(self.DAY_GROUP, self._increment_day)
        self.date.SetDownHandler(self.YEAR_GROUP, self._decrement_year)
        self.date.SetDownHandler(self.MONTH_GROUP, self._decrement_month)
        self.date.SetDownHandler(self.DAY_GROUP, self._decrement_day)

    def _is_date_valid(self):
        return self._get_date() is not None

    def _increment_year(self):
        date = self._get_date()
        self._write_date(self._set_valid_day(date.year + 1, date.month, date.day))

    def _increment_month(self):
        date = self._get_date()
        self._write_date(self._set_valid_day(date.year, date.month + 1, date.day))

    def _increment_day(self):
        date = self._get_date()
        self._write_date(self._set_valid_day(date.year, date.month, date.day + 1))

    def _decrement_year(self):
        date = self._get_date()
        self._write_date(self._set_valid_day(date.year - 1, date.month, date.day))

    def _decrement_month(self):
        date = self._get_date()
        self._write_date(self._set_valid_day(date.year, date.month - 1, date.day))

    def _decrement_day(self):
        date = self._get_date()
        self._write_date(self._set_valid_day(date.year, date.month, date.day - 1))

    def _get_date(self):
        try:
            [year_str, month_str, day_str] = self.date.GetParts()
            return datetime.date(int(year_str), int(month_str), int(day_str))
        except:
            return None

    def _write_date(self, date):
        if date is not None:
            self.date.SetParts([
                "%04d" % date.year,
                "%02d" % date.month,
                "%02d" % date.day,
            ])

    def _set_valid_day(self, year, month, day):
        while True:
            if day <= 0:
                return None
            try:
                return datetime.date(year, month, day)
            except:
                day -= 1
