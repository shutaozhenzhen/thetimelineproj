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

from timelinelib.canvas.drawing.interface import Strip
from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.calendar.gregorian.timetype.yearformatter import format_year


class StripYear(Strip):

    def label(self, time, major=False):
        return format_year(GregorianDateTime.from_time(time).year)

    def start(self, time):
        gregorian_time = GregorianDateTime.from_time(time)
        new_gregorian = GregorianDateTime.from_ymd(gregorian_time.year, 1, 1)
        return new_gregorian.to_time()

    def increment(self, time):
        gregorian_time = GregorianDateTime.from_time(time)
        return gregorian_time.replace(year=gregorian_time.year + 1).to_time()
