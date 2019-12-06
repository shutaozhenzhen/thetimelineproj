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


class StripDecade(Strip):

    """
    Year Name | Year integer | Decade name
    ----------+--------------+------------
    ..        |  ..          |
    20 BC     | -19          | 20s BC (10 years)
    ----------+--------------+------------
    19 BC     | -18          |
    18 BC     | -17          |
    17 BC     | -16          |
    16 BC     | -15          |
    15 BC     | -14          | 10s BC (10 years)
    14 BC     | -13          |
    13 BC     | -12          |
    12 BC     | -11          |
    11 BC     | -10          |
    10 BC     | -9           |
    ----------+--------------+------------
    9  BC     | -8           |
    8  BC     | -7           |
    7  BC     | -6           |
    6  BC     | -5           |
    5  BC     | -4           | 0s BC (only 9 years)
    4  BC     | -3           |
    3  BC     | -2           |
    2  BC     | -1           |
    1  BC     |  0           |
    ----------+--------------+------------
    1         |  1           |
    2         |  2           |
    3         |  3           |
    4         |  4           |
    5         |  5           |  0s (only 9 years)
    6         |  6           |
    7         |  7           |
    8         |  8           |
    9         |  9           |
    ----------+--------------+------------
    10        |  10          |
    11        |  11          |
    12        |  12          |
    13        |  13          |
    14        |  14          |
    15        |  15          |  10s (10 years)
    16        |  16          |
    17        |  17          |
    18        |  18          |
    19        |  19          |
    ----------+--------------+------------
    20        |  20          |  20s (10 years)
    ..        |  ..          |
    """

    def __init__(self):
        self.skip_s_in_decade_text = False

    def label(self, time, major=False):
        coptic_time = CopticDateTime.from_time(time)
        return self._format_decade(
            self._decade_number(self._decade_start_year(coptic_time.year)),
            coptic_time.is_bc()
        )

    def start(self, time):
        return CopticDateTime.from_ymd(
            self._decade_start_year(CopticDateTime.from_time(time).year),
            1,
            1
        ).to_time()

    def increment(self, time):
        coptic_time = CopticDateTime.from_time(time)
        return coptic_time.replace(
            year=self._next_decacde_start_year(coptic_time.year)
        ).to_time()

    def set_skip_s_in_decade_text(self, value):
        self.skip_s_in_decade_text = value

    def _format_decade(self, decade_number, is_bc):
        parts = []
        parts.append("{0}".format(decade_number))
        if not self.skip_s_in_decade_text:
            parts.append("s")
        if is_bc:
            parts.append(" ")
            parts.append(BC)
        return "".join(parts)

    def _decade_start_year(self, year):
        if year > 9:
            return int(year) - (int(year) % 10)
        elif year >= 1:
            return 1
        elif year >= -8:
            return -8
        else:  # year < -8
            return -self._decade_start_year(-year + 1) - 8

    def _next_decacde_start_year(self, start_year):
        return start_year + self._decade_year_len(start_year)

    def _decade_year_len(self, start_year):
        if self._decade_number(start_year) == 0:
            return 9
        else:
            return 10

    def _decade_number(self, start_year):
        if start_year > 9:
            return start_year
        elif start_year >= -8:
            return 0
        else:  # start_year < -8
            return self._decade_number(-start_year - 8)
