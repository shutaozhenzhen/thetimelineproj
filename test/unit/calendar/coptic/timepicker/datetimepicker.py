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


from unittest.mock import Mock

from timelinelib.calendar.coptic.coptic import CopticDateTime
from timelinelib.calendar.coptic.timepicker.datepicker import CopticDatePicker
from timelinelib.calendar.coptic.timepicker.datetimepicker import CopticDateTimePicker
from timelinelib.calendar.generic.timepicker.datetimepickercontroller import DateTimePickerController
from timelinelib.calendar.coptic.timepicker.datetimepicker import CopticTimePicker
from timelinelib.test.cases.unit import UnitTestCase


class ACopticDateTimePicker(UnitTestCase):

    def setUp(self):
        self.view = Mock(CopticDateTimePicker)
        self.date_picker = Mock(CopticDatePicker)
        self.time_picker = Mock(CopticTimePicker)
        self.now_fn = Mock()
        self.controller = DateTimePickerController(
            self.view, CopticDateTime, self.date_picker, self.time_picker, self.now_fn, None)

    def testDateControlIsAssignedDatePartFromSetValue(self):
        self.controller.set_value(CopticDateTime(2010, 11, 20, 15, 33, 0).to_time())
        self.date_picker.SetDate.assert_called_with((2010, 11, 20))

    # TODO: Is this really CopticDateTimePicker's responsibility?
    def testDateControlIsAssignedCurrentDateIfSetWithValueNone(self):
        self.now_fn.return_value = CopticDateTime(2010, 8, 30, 0, 0, 0).to_time()
        self.controller.set_value(None)
        self.date_picker.SetDate.assert_called_with((2010, 8, 30))

    def testTimeControlIsAssignedTimePartFromSetValue(self):
        self.controller.set_value(CopticDateTime(2010, 11, 20, 15, 33, 0).to_time())
        self.time_picker.SetTime.assert_called_with((15, 33, 0))

    # TODO: Is this really CopticDateTimePicker's responsibility?
    def testTimeControlIsAssignedCurrentTimeIfSetWithValueNone(self):
        self.now_fn.return_value = CopticDateTime(2010, 8, 30, 12, 15, 0).to_time()
        self.controller.set_value(None)
        self.time_picker.SetTime.assert_called_with((12, 15, 0))

    def testGetValueWhenTimeIsShownShouldReturnDateWithTime(self):
        self.time_picker.IsShown.return_value = True
        self.time_picker.GetTime.return_value = (14, 30, 0)
        self.date_picker.GetDate.return_value = (2010, 8, 30)
        self.assertEqual(CopticDateTime(2010, 8, 30, 14, 30, 0).to_time(), self.controller.get_value())

    def testGetValueWhenTimeIsHiddenShouldReturnDateWithoutTime(self):
        self.time_picker.IsShown.return_value = False
        self.time_picker.GetTime.return_value = (14, 30, 0)
        self.date_picker.GetDate.return_value = (2010, 8, 30)
        self.assertEqual(CopticDateTime(2010, 8, 30, 0, 0, 0).to_time(), self.controller.get_value())

    def testControllerCanConverDateTupleToWxDate(self):
        wx_date = self.controller.date_tuple_to_wx_date((2010, 8, 30))
        self.assertEqual((2010, 8, 30), (wx_date.year, wx_date.month + 1, wx_date.day))

    def testControllerCanConverWxdateToDateTuple(self):
        wx_date = self.controller.date_tuple_to_wx_date((2010, 8, 30))
        year, month, day = self.controller.wx_date_to_date_tuple(wx_date)
        self.assertEqual((2010, 8, 30), (year, month, day))
