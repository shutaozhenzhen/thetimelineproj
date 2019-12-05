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
from timelinelib.calendar.bosparanian.bosparanian import BosparanianDateTime
from timelinelib.calendar.bosparanian.time import BosparanianDelta
from timelinelib.calendar.bosparanian.timetype.strips.stripyear import format_year
from timelinelib.calendar.bosparanian.monthnames import bosp_abbreviated_name_of_month


class StripWeek(Strip):

    def __init__(self):
        Strip.__init__(self)

    def label(self, time, major=False):
        if major:
            first_weekday = self.start(time)
            next_first_weekday = self.increment(first_weekday)
            last_weekday = next_first_weekday - BosparanianDelta.from_days(1)
            range_string = self._time_range_string(first_weekday, last_weekday)
            return (_("Week") + " %s (%s)") % (BosparanianDateTime.from_time(time).week_number, range_string)
        return _("Week") + " %s" % BosparanianDateTime.from_time(time).week_number

    @staticmethod
    def _time_range_string(start, end):
        start = BosparanianDateTime.from_time(start)
        end = BosparanianDateTime.from_time(end)
        if start.year == end.year:
            if start.month == end.month:
                return "%s-%s %s %s" % (start.day, end.day,
                                        bosp_abbreviated_name_of_month(start.month),
                                        format_year(start.year))
            return "%s %s-%s %s %s" % (start.day,
                                       bosp_abbreviated_name_of_month(start.month),
                                       end.day,
                                       bosp_abbreviated_name_of_month(end.month),
                                       format_year(start.year))
        return "%s %s %s-%s %s %s" % (start.day,
                                      bosp_abbreviated_name_of_month(start.month),
                                      format_year(start.year),
                                      end.day,
                                      bosp_abbreviated_name_of_month(end.month),
                                      format_year(end.year))

    def start(self, time):
        from timelinelib.calendar.bosparanian.timetype.timetype import BosparanianTimeType
        from timelinelib.calendar.bosparanian.time import BosparanianTime
        days_to_subtract = BosparanianTimeType().get_day_of_week(time)
        return BosparanianTime(time.julian_day - days_to_subtract, 0)

    def increment(self, time):
        return time + BosparanianDelta.from_days(7)
