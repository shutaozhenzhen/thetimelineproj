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
from timelinelib.calendar.generic.timepicker.datemodifier import DateModifier
from timelinelib.calendar.generic.timepicker.datepicker import DatePicker
from timelinelib.calendar.generic.timepicker.datetimepicker import DateTimePicker
from timelinelib.calendar.generic.timepicker.timepicker import TimePicker
from timelinelib.calendar.pharaonic.timetype.timetype import PharaonicTimeType
from timelinelib.calendar.pharaonic.pharaonic import PharaonicDateTime
from timelinelib.calendar.pharaonic.dateformatter import PharaonicDateFormatter
from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.calendar.pharaonic.pharaonic import is_valid_time
from timelinelib.config.dateformatparser import DateFormatParser


class PharaonicDateTimePicker(DateTimePicker):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        DateTimePicker.__init__(self, parent, show_time, config, on_change)
        self._time_type = PharaonicTimeType()
        date_modifier = DateModifier(PharaonicTimeType(), PharaonicDelta, PharaonicDateTime, max_month=13)
        self._date_picker = DatePicker(self, date_modifier, self._get_date_formatter(), on_change)
        self._time_picker = TimePicker(self, False, separators=[":"], validator_function=is_valid_time)
        self._controller = DateTimePickerController(self, PharaonicDateTime, self._date_picker, self._time_picker,
                                                    PharaonicTimeType().now, on_change)
        self.create_gui()
        self.show_time(show_time)

    def _get_date_formatter(self):
        parser = DateFormatParser().parse(self._config.get_date_format())
        date_formatter = PharaonicDateFormatter()
        date_formatter.set_defaults(self._config.use_date_default_values,
                                    self._config.default_year,
                                    self._config.default_month,
                                    self._config.default_day)
        date_formatter.set_separators(*parser.get_separators())
        date_formatter.set_region_order(*parser.get_region_order())
        date_formatter.use_abbreviated_name_for_month(parser.use_abbreviated_month_names())
        return date_formatter
