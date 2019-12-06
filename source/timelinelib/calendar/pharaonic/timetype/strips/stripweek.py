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


from timelinelib.calendar.pharaonic.pharaonic import PharaonicDateTime
from timelinelib.calendar.pharaonic.monthnames import abbreviated_name_of_month
from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.canvas.drawing.interface import Strip
from timelinelib.calendar.pharaonic.timetype.formatters import format_year


class StripWeek(Strip):

    def __init__(self, appearance):
        Strip.__init__(self)
        self.appearance = appearance

    def label(self, time, major=False):
        if major:
            first_weekday = self.start(time)
            next_first_weekday = self.increment(first_weekday)
            last_weekday = next_first_weekday - PharaonicDelta.from_days(1)
            range_string = self._time_range_string(first_weekday, last_weekday)
            if self.appearance.get_week_start() == "tkyriaka":
                return (_("Week") + " %s (%s)") % (
                    PharaonicDateTime.from_time(time).week_number,
                    range_string
                )
            else:
                # It is Psabbaton (don't know what to do about week numbers here)
                return range_string
        # This strip should never be used as minor
        return ""

    @staticmethod
    def _time_range_string(start, end):
        start = PharaonicDateTime.from_time(start)
        end = PharaonicDateTime.from_time(end)
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
