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


class DateModifier:

    MAX_MONTH = 12

    def __init__(self):
        self._time_type = None
        self._delta = None
        self._date_time = None

    def increment_year(self, date):
        max_year = self._date_time.from_time(self._time_type.get_max_time()).year
        year, month, day = date
        if year < max_year - 1:
            return self._set_valid_day(year + 1, month, day)
        return date

    def increment_month(self, date):
        max_year = self._date_time.from_time(self._time_type.get_max_time()).year
        year, month, day = date
        if month < self.MAX_MONTH:
            return self._set_valid_day(year, month + 1, day)
        elif year < max_year - 1:
            return self._set_valid_day(year + 1, 1, day)
        return date

    def increment_day(self, date):
        year, month, day = date
        time = self._date_time.from_ymd(year, month, day).to_time()
        if time < self._time_type.get_max_time() - self._delta.from_days(1):
            return self._date_time.from_time(time + self._delta.from_days(1)).to_date_tuple()
        return date

    def decrement_year(self, date):
        year, month, day = date
        if year > self._date_time.from_time(self._time_type.get_min_time()).year:
            return self._set_valid_day(year - 1, month, day)
        return date

    def decrement_month(self, date):
        year, month, day = date
        if month > 1:
            return self._set_valid_day(year, month - 1, day)
        elif year > self._date_time.from_time(self._time_type.get_min_time()).year:
            return self._set_valid_day(year - 1, self.MAX_MONTH, day)
        return date

    def decrement_day(self, date):
        year, month, day = date
        if day > 1:
            return self._set_valid_day(year, month, day - 1)
        elif month > 1:
            return self._set_valid_day(year, month - 1, 31)
        elif year > self._date_time.from_time(self._time_type.get_min_time()).year:
            return self._set_valid_day(year - 1, self.MAX_MONTH, 31)
        return date

    def _set_valid_day(self, new_year, new_month, new_day):
        done = False
        date = None
        while not done:
            try:
                date = self._date_time.from_ymd(new_year, new_month, new_day)
                done = True
            except Exception:
                new_day -= 1
        return date.to_date_tuple()
