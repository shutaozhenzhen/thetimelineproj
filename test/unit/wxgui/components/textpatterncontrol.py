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


import datetime

import humblewx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.framework import Dialog


class describe_text_pattern_control(UnitTestCase):

    def test_it_shows_in_dialog(self):
        self.show_dialog(TestDialog)


class TestDialog(Dialog):

    """
    <BoxSizerVertical>
        <Button label="before" />
        <TextPatternControl name="date" />
        <Button label="after" />
    </BoxSizerVertical>
    """

    class Controller(humblewx.Controller):

        def values_validator(self, view):
            return self._values_to_date(view.GetValues()) is not None

        def up_handler(self, view):
            date = self._values_to_date(view.GetValues())
            if view.GetSelectedGroup() == 0:
                self._write_date(view, self._set_valid_day(date.year + 1, date.month, date.day))
            elif view.GetSelectedGroup() == 1:
                self._write_date(view, self._set_valid_day(date.year, date.month + 1, date.day))
            elif view.GetSelectedGroup() == 2:
                self._write_date(view, self._set_valid_day(date.year, date.month, date.day + 1))

        def down_handler(self, view):
            date = self._values_to_date(view.GetValues())
            if view.GetSelectedGroup() == 0:
                self._write_date(view, self._set_valid_day(date.year - 1, date.month, date.day))
            elif view.GetSelectedGroup() == 1:
                self._write_date(view, self._set_valid_day(date.year, date.month - 1, date.day))
            elif view.GetSelectedGroup() == 2:
                self._write_date(view, self._set_valid_day(date.year, date.month, date.day - 1))

        def _values_to_date(self, values):
            try:
                [year_str, month_str, day_str] = values
                return datetime.date(int(year_str), int(month_str), int(day_str))
            except:
                return None

        def _write_date(self, view, date):
            if date is not None:
                view.SetValues(["%04d" % date.year, "%02d" % date.month, "%02d" % date.day])

        def _set_valid_day(self, year, month, day):
            while True:
                if day <= 0:
                    return None
                try:
                    return datetime.date(year, month, day)
                except:
                    day -= 1

    def __init__(self):
        Dialog.__init__(self, self.Controller, None, {
        })
        self.date.SetSeparators(["-", "-"])
        self.date.SetValues(["2015", "12", "05"])
        self.date.SetValuesValidator(self.controller.values_validator)
        self.date.SetUpHandler(self.controller.up_handler)
        self.date.SetDownHandler(self.controller.down_handler)
