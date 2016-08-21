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


from mock import Mock
from mock import sentinel

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.time.typeinterface import TimeType
from timelinelib.wxgui.components.timepickerwrapper.controller import TimePickerWrapperController
from timelinelib.wxgui.components.timepickerwrapper.view import TimePickerWrapper


class TimePickerWrapperControllerTestCase(UnitTestCase):

    def setUp(self):
        self.view = Mock(TimePickerWrapper)
        self.controller = TimePickerWrapperController(self.view)
        self.time_type = Mock(TimeType)
        self.time_picker = Mock()
        self.given_times_in_range([])
        self.controller.on_init(self.time_type, self.time_picker)

    def given_times_in_range(self, values):
        def is_time_in_range(time):
            return time in values
        self.time_type.is_time_in_range.side_effect = is_time_in_range


class describe_init(TimePickerWrapperControllerTestCase):

    def test_shows_time_picker(self):
        self.assertEqual(self.view.ShowTimePicker.call_count, 1)


class describe_set_value(TimePickerWrapperControllerTestCase):

    def test_forwards_call_when_time_is_in_range(self):
        self.given_times_in_range([sentinel.VALUE])
        self.controller.set_value(sentinel.VALUE)
        self.time_picker.set_value.assert_called_with(sentinel.VALUE)

    def test_does_not_forward_when_time_is_out_of_range(self):
        self.controller.set_value(sentinel.VALUE)
        self.assertEqual(self.time_picker.set_value.call_count, 0)

    def test_shows_time_picker_when_time_is_in_range(self):
        self.given_times_in_range([sentinel.VALUE])
        self.controller.set_value(sentinel.VALUE)
        self.assertTimePickerIsShown()

    def test_shows_out_of_range_message_when_time_is_out_of_range(self):
        self.controller.set_value(sentinel.VALUE)
        self.assertOutOfRangeControlIsShown()

    def assertTimePickerIsShown(self):
        self.assertEqual(self.view.ShowTimePicker.call_count, 2) # 1 for init
        self.assertEqual(self.view.ShowOutOfRangeControl.call_count, 0)

    def assertOutOfRangeControlIsShown(self):
        self.assertEqual(self.view.ShowTimePicker.call_count, 1) # 1 for init
        self.assertEqual(self.view.ShowOutOfRangeControl.call_count, 1)


class describe_get_value(TimePickerWrapperControllerTestCase):

    def test_forwards_call_after_init(self):
        self.time_picker.get_value.return_value = sentinel.VALUE
        self.assertEqual(self.controller.get_value(), sentinel.VALUE)

    def test_forwards_call_when_in_range_time_has_been_set(self):
        self.given_times_in_range([sentinel.VALUE])
        self.controller.set_value(sentinel.VALUE)
        self.time_picker.get_value.return_value = sentinel.ANOTHER_VALUE
        self.assertEqual(self.controller.get_value(), sentinel.ANOTHER_VALUE)

    def test_get_previously_set_when_out_range_time_has_been_set(self):
        self.controller.set_value(sentinel.VALUE)
        self.time_picker.get_value.return_value = sentinel.ANOTHER_VALUE
        self.assertEqual(self.controller.get_value(), sentinel.VALUE)

    def test_forwars_call_when_out_in_time_range_has_been_set(self):
        self.given_times_in_range([sentinel.VALUE2])
        self.controller.set_value(sentinel.VALUE1) # out of range
        self.controller.set_value(sentinel.VALUE2) # in range
        self.time_picker.get_value.return_value = sentinel.ANOTHER_VALUE
        self.assertEqual(self.controller.get_value(), sentinel.ANOTHER_VALUE)


class describe_show_time(TimePickerWrapperControllerTestCase):

    def test_forwards_show_time(self):
        self.controller.show_time(sentinel.SHOW)
        self.time_picker.show_time.assert_called_with(sentinel.SHOW)
