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

from timelinelib.calendar.generic.timepicker.datepicker import DatePicker
from timelinelib.calendar.generic.timepicker.datetimepickercontroller import DateTimePickerController
from timelinelib.calendar.generic.timepicker.datetimepicker import DateTimePicker
from timelinelib.calendar.generic.timepicker.datemodifier import DateModifier
from timelinelib.calendar.coptic.timepicker.timepicker import CopticTimePicker
from timelinelib.calendar.coptic.dateformatter import CopticDateFormatter
from timelinelib.calendar.coptic.timetype.timetype import CopticTimeType
from timelinelib.calendar.coptic.coptic import CopticDateTime
from timelinelib.calendar.coptic.time import CopticDelta


class CopticDateTimePicker(DateTimePicker):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        DateTimePicker.__init__(self, parent, show_time, config, on_change)
        self._time_type = CopticTimeType()
        date_modifier = DateModifier(CopticTimeType(), CopticDelta, CopticDateTime, max_month=13)
        self._date_picker = DatePicker(self, date_modifier, CopticDateFormatter(), on_change)
        self._time_picker = CopticTimePicker(self)
        self._controller = DateTimePickerController(self, CopticDateTime, self._date_picker, self._time_picker,
                                                    CopticTimeType().now, on_change)
        self.create_gui()
        self.show_time(show_time)
