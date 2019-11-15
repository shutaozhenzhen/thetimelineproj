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


class DurationFormatter:

    def __init__(self, duration):
        """Duration is a list containing days and seconds like [days, seconds]."""
        self._duration = duration

    def format(self, duration_parts):
        """
        Return a string describing a time duration. Such a string
        can look like::

            2 years 1 month 3 weeks

        The argument duration_parts is a tuple where each element
        describes a duration type like YEARS, WEEKS etc.
        """
        values = self._calc_duration_values(duration_parts)
        return self._format_parts(zip(values, duration_parts))

    def _calc_duration_values(self, duration_parts):
        values = []
        for duration_part in duration_parts:
            value = duration_part.value_fn(self._duration)
            self._duration[0], self._duration[1] = duration_part.remainder_fn(self._duration)
            values.append(value)
        return values

    def _format_parts(self, duration_parts):
        durations = self._remov_zero_value_parts(duration_parts)
        return " ". join(self._format_durations_parts(durations))

    @staticmethod
    def _remov_zero_value_parts(duration_parts):
        return [duration for duration in duration_parts
                if duration[0] > 0]

    def _format_durations_parts(self, durations):
        return [self._format_part(duration_value, duration_type) for
                duration_value, duration_type in durations]

    @staticmethod
    def _format_part(value, duration_type):
        if value == 1:
            heading = duration_type.single_name
        else:
            heading = duration_type.name
        return f'{value} {heading}'
