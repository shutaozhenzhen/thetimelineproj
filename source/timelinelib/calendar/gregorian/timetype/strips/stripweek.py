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
from timelinelib.calendar.gregorian.time import GregorianTime


class StripWeek(Strip):

    def __init__(self, appearance):
        Strip.__init__(self)
        self.appearance = appearance

    def label(self, time, major=False):
        if major:
            first_weekday = self.start(time)
            next_first_weekday = self.increment(first_weekday)
            last_weekday = next_first_weekday - GregorianDelta.from_days(1)
            range_string = self._time_range_string(first_weekday, last_weekday)
            if self.appearance.get_week_start() == "monday":
                return (_("Week") + " %s (%s)") % (
                    GregorianDateTime.from_time(time).week_number,
                    range_string
                )
            else:
                # It is sunday (don't know what to do about week numbers here)
                return range_string
        # This strip should never be used as minor
        return ""

    def _time_range_string(self, start, end):
        start = GregorianDateTime.from_time(start)
        end = GregorianDateTime.from_time(end)
        if start.year == end.year:
            if start.month == end.month:
                return "%s-%s %s %s" % (start.day, end.day,
                                        abbreviated_name_of_month(start.month),
                                        format_year(start.year))
            return "%s %s-%s %s %s" % (start.day,
                                       abbreviated_name_of_month(start.month),
                                       end.day,
                                       abbreviated_name_of_month(end.month),
                                       format_year(start.year))
        return "%s %s %s-%s %s %s" % (start.day,
                                      abbreviated_name_of_month(start.month),
                                      format_year(start.year),
                                      end.day,
                                      abbreviated_name_of_month(end.month),
                                      format_year(end.year))

    def start(self, time):
        if self.appearance.get_week_start() == "monday":
            days_to_subtract = time.day_of_week
        else:
            # It is sunday
            days_to_subtract = (time.day_of_week + 1) % 7
        return GregorianTime(time.julian_day - days_to_subtract, 0)

    def increment(self, time):
        return time + GregorianDelta.from_days(7)


