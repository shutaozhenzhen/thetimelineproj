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


import humblewx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.time.timeline import Time
from timelinelib.wxgui.framework import Dialog


class TimePickerWrapperTestCase(UnitTestCase):

    def test_show_manual_test_dialog(self):
        self.show_dialog(TimePickerWrapperTestDialog)


class TimePickerWrapperTestDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="1" border="ALL">
            <Button label="before" />
            <TimePicker name="time_picker_before" time_type="$(time_type)" />
            <TimePicker name="time_picker" time_type="$(time_type)" />
            <TimePicker name="time_picker_after" time_type="$(time_type)" />
            <Button label="after" />
        </FlexGridSizer>
    </BoxSizerVertical>
    """

    def __init__(self):
        Dialog.__init__(self, humblewx.Controller, None, {
            "time_type": RestrictedGregorianTimeType(),
        })
        self.time_picker_before.set_value(Time(0, 0))
        self.time_picker.set_value(Time(1500000, 0))
        self.time_picker_after.set_value(Time(3000000, 0))


class RestrictedGregorianTimeType(GregorianTimeType):

    def get_min_time(self):
        return (Time(1000000, 0), "1M")

    def get_max_time(self):
        return (Time(2000000, 0), "2M")
