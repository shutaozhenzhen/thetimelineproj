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


class TimePickerWrapperController(object):

    def __init__(self, view):
        self._view = view

    def on_init(self, time_type, time_picker):
        self._time_type = time_type
        self._time_picker = time_picker
        self._show_time_picker()

    def set_value(self, value):
        if self._time_type.is_time_in_range(value):
            self._time_picker.set_value(value)
            self._show_time_picker()
        else:
            self._show_out_of_range(value)

    def get_value(self):
        if self._out_of_range_value is None:
            return self._time_picker.get_value()
        else:
            return self._out_of_range_value

    def show_time(self, show):
        self._time_picker.show_time(show)

    def _show_time_picker(self):
        self._out_of_range_value = None
        self._view.ShowTimePicker()

    def _show_out_of_range(self, value):
        self._out_of_range_value = value
        self._view.ShowOutOfRangeControl()
