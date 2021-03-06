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
from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.monthnames import abbreviated_name_of_month
from timelinelib.calendar.gregorian.timetype.yearformatter import format_year


class StripDay(Strip):

    def label(self, time, major=False):
        time = GregorianDateTime.from_time(time)
        if major:
            return "%s %s %s" % (time.day,
                                 abbreviated_name_of_month(time.month),
                                 format_year(time.year))
        return str(time.day)

    def start(self, time):
        gregorian_time = GregorianDateTime.from_time(time)
        return GregorianDateTime.from_ymd(
            gregorian_time.year,
            gregorian_time.month,
            gregorian_time.day
        ).to_time()

    def increment(self, time):
        return time + GregorianDelta.from_days(1)

    def is_day(self):
        return True
