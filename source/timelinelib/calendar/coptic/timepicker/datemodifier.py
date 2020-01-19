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


from timelinelib.calendar.coptic.coptic import CopticDateTime
from timelinelib.calendar.coptic.time import CopticDelta
from timelinelib.calendar.coptic.timetype.timetype import CopticTimeType
import timelinelib.calendar.generic.timepicker.datemodifier as generic


class DateModifier(generic.DateModifier):

    def __init__(self):
        self._time_type = CopticTimeType()
        self._delta = CopticDelta
        self._date_time = CopticDateTime

    def increment_month(self, date):
        max_year = self._date_time.from_time(self._time_type.get_max_time()).year
        year, month, day = date
        if month < 13:
            return self._set_valid_day(year, month + 1, day)
        elif year < max_year - 1:
            return self._set_valid_day(year + 1, 1, day)
        return date

    def decrement_month(self, date):
        year, month, day = date
        if month > 1:
            return self._set_valid_day(year, month - 1, day)
        elif year > self._date_time.from_time(self._time_type.get_min_time()).year:
            return self._set_valid_day(year - 1, 13, day)
        return date

    def decrement_day(self, date):
        year, month, day = date
        if day > 1:
            return self._set_valid_day(year, month, day - 1)
        elif month > 1:
            return self._set_valid_day(year, month - 1, 30)
        elif year > self._date_time.from_time(self._time_type.get_min_time()).year:
            return self._set_valid_day(year - 1, 12, 30)
        return date
