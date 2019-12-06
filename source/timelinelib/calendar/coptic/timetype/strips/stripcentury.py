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
from timelinelib.canvas.drawing.interface import Strip
from timelinelib.calendar.coptic.timetype.formatters import BC


class StripCentury(Strip):

    """
    Year Name | Year integer | Decade name
    ----------+--------------+------------
    ..        |  ..          |
    200 BC    | -199         | 200s BC (100 years)
    ----------+--------------+------------
    199 BC    | -198         |
    ...       | ...          | 100s BC (100 years)
    100 BC    | -99          |
    ----------+--------------+------------
    99  BC    | -98          |
    ...       |  ...         | 0s BC (only 99 years)
    1   BC    |  0           |
    ----------+--------------+------------
    1         |  1           |
    ...       |  ...         | 0s (only 99 years)
    99        |  99          |
    ----------+--------------+------------
    100       |  100         |
    ..        |  ..          | 100s (100 years)
    199       |  199         |
    ----------+--------------+------------
    200       |  200         | 200s (100 years)
    ..        |  ..          |
    """

    def label(self, time, major=False):
        if major:
            coptic_time = CopticDateTime.from_time(time)
            return self._format_century(
                self._century_number(
                    self._century_start_year(coptic_time.year)
                ),
                coptic_time.is_bc()
            )
        else:
            return ""

    def start(self, time):
        return CopticDateTime.from_ymd(
            self._century_start_year(CopticDateTime.from_time(time).year),
            1,
            1
        ).to_time()

    def increment(self, time):
        coptic_time = CopticDateTime.from_time(time)
        return coptic_time.replace(
            year=self._next_century_start_year(coptic_time.year)
        ).to_time()

    def _century_number(self, century_start_year):
        if century_start_year > 99:
            return century_start_year
        elif century_start_year >= -98:
            return 0
        else:  # century_start_year < -98:
            return self._century_number(-century_start_year - 98)

    def _next_century_start_year(self, start_year):
        return start_year + self._century_year_len(start_year)

    @staticmethod
    def _century_year_len(start_year):
        if start_year in [-98, 1]:
            return 99
        else:
            return 100

    @staticmethod
    def _format_century(century_number, is_bc):
        if is_bc:
            return "{century}s {bc}".format(century=century_number, bc=BC)
        else:
            return "{century}s".format(century=century_number)

    def _century_start_year(self, year):
        if year > 99:
            return year - int(year) % 100
        elif year >= 1:
            return 1
        elif year >= -98:
            return -98
        else:  # year < -98
            return -self._century_start_year(-year + 1) - 98


