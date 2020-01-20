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


from timelinelib.calendar.generic.timepicker.datetimepickercontroller import DateTimePickerController
from timelinelib.calendar.generic.timepicker.datetimepicker import DateTimePicker
from timelinelib.calendar.generic.timepicker.datepicker import DatePicker
from timelinelib.calendar.generic.timepicker.datemodifier import DateModifier
from timelinelib.calendar.generic.timepicker.timepicker import TimePicker
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.gregorian import is_valid_time


class GregorianDateTimePicker(DateTimePicker):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        DateTimePicker.__init__(self, parent, show_time, config, on_change)
        self._time_type = GregorianTimeType()
        date_modifier = DateModifier(GregorianTimeType(), GregorianDelta, GregorianDateTime)
        self._date_picker = DatePicker(self, date_modifier, GregorianDateFormatter(), on_change)
        self._time_picker = self._create_time_picker(config)
        self._controller = DateTimePickerController(self, GregorianDateTime, self._date_picker, self._time_picker,
                                                    GregorianTimeType().now, on_change)
        self.create_gui()
        self.show_time(show_time)

    def _create_time_picker(self, config):
        if config.use_second:
            separators = [":", ":"]
        else:
            separators = [":"]
        return TimePicker(self, config.use_second, separators=separators, validator_function=is_valid_time)
