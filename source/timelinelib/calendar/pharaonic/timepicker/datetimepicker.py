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


import os.path

import wx.adv

from timelinelib.calendar.pharaonic.timepicker.datepicker import PharaonicDatePicker
from timelinelib.calendar.pharaonic.timepicker.timepicker import PharaonicTimePicker
from timelinelib.calendar.generic.timepicker.calendarpopup import CalendarPopup
from timelinelib.calendar.pharaonic.timepicker.datetimepickercontroller import PharaonicDateTimePickerController
from timelinelib.calendar.pharaonic.timetype.timetype import PharaonicTimeType
from timelinelib.config.paths import ICONS_DIR
from timelinelib.calendar.generic.timepicker.datetimepicker import DateTimePicker


class PharaonicDateTimePicker(DateTimePicker):

    def __init__(self, parent, show_time=True, config=None, on_change=None):
        DateTimePicker.__init__(self, parent, show_time, config, on_change)
        self._time_type = PharaonicTimeType()
        self._date_picker = PharaonicDatePicker(self, config.get_date_formatter(), on_change=on_change)
        self._time_picker = PharaonicTimePicker(self)
        self._controller = PharaonicDateTimePickerController(self, self._date_picker, self._time_picker,
                                                             PharaonicTimeType().now, on_change)
        self.create_gui()
        self.show_time(show_time)
