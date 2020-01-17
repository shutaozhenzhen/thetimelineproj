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


import humblewx

from timelinelib.calendar.pharaonic.dateformatter import PharaonicDateFormatter
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.framework import Dialog
import timelinelib.calendar.pharaonic.timepicker.datepicker as pdp


class describe_new_pharaonic_date_picker_view(UnitTestCase):

    def test_show_manual_test_dialog(self):
        try:
            humblewx.COMPONENT_MODULES.insert(0, pdp)
            self.show_dialog(NewPharaonicDatePickerTestDialog)
        finally:
            humblewx.COMPONENT_MODULES.remove(pdp)


class NewPharaonicDatePickerTestDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="1" border="ALL">
            <Button label="before" />
            <PharaonicDatePicker
                date_formatter="$(date_formatter)"
                name="date"
            />
            <Button label="after" />
        </FlexGridSizer>
    </BoxSizerVertical>
    """

    def __init__(self):
        Dialog.__init__(self, humblewx.Controller, None, {
            "date_formatter": self._create_date_formatter()
        })
        self.date.SetDate((2015, 11, 1))

    def _create_date_formatter(self):
        formatter = PharaonicDateFormatter()
        formatter.set_separators("/", " ")
        formatter.set_region_order(year=2, month=1, day=0)
        return formatter
