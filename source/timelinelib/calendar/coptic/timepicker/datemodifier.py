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


class DateModifier:

    def increment_year(self, date):
        max_year = CopticDateTime.from_time(CopticTimeType().get_max_time()).year
        year, month, day = date
        if year < max_year - 1:
            return self._set_valid_day(year + 1, month, day)
        return date

    def increment_month(self, date):
        max_year = CopticDateTime.from_time(CopticTimeType().get_max_time()).year
        year, month, day = date
        if month < 13:
            return self._set_valid_day(year, month + 1, day)
        elif year < max_year - 1:
            return self._set_valid_day(year + 1, 1, day)
        return date

    @staticmethod
    def increment_day(date):
        year, month, day = date
        time = CopticDateTime.from_ymd(year, month, day).to_time()
        if time < CopticTimeType().get_max_time() - CopticDelta.from_days(1):
            return CopticDateTime.from_time(time + CopticDelta.from_days(1)).to_date_tuple()
        return date

    def decrement_year(self, date):
        year, month, day = date
        if year > CopticDateTime.from_time(CopticTimeType().get_min_time()).year:
            return self._set_valid_day(year - 1, month, day)
        return date

    def decrement_month(self, date):
        year, month, day = date
        if month > 1:
            return self._set_valid_day(year, month - 1, day)
        elif year > CopticDateTime.from_time(CopticTimeType().get_min_time()).year:
            return self._set_valid_day(year - 1, 13, day)
        return date

    def decrement_day(self, date):
        year, month, day = date
        if day > 1:
            return self._set_valid_day(year, month, day - 1)
        elif month > 1:
            return self._set_valid_day(year, month - 1, 30)
        elif year > CopticDateTime.from_time(CopticTimeType().get_min_time()).year:
            return self._set_valid_day(year - 1, 12, 30)
        return date

    @staticmethod
    def _set_valid_day(new_year, new_month, new_day):
        done = False
        date = None
        while not done:
            try:
                date = CopticDateTime.from_ymd(new_year, new_month, new_day)
                done = True
            except Exception:
                new_day -= 1
        return date.to_date_tuple()
