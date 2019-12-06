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
from timelinelib.calendar.coptic.monthnames import abbreviated_name_of_month
from timelinelib.calendar.coptic.time import CopticDelta
from timelinelib.calendar.coptic.weekdaynames import abbreviated_name_of_weekday
from timelinelib.canvas.drawing.interface import Strip
from timelinelib.calendar.coptic.timetype.formatters import format_year, get_day_of_week


class StripWeekday(Strip):

    def label(self, time, major=False):
        day_of_week = get_day_of_week(time)
        if major:
            time = CopticDateTime.from_time(time)
            return "%s %s %s %s" % (abbreviated_name_of_weekday(day_of_week),
                                    time.day,
                                    abbreviated_name_of_month(time.month),
                                    format_year(time.year))
        return (abbreviated_name_of_weekday(day_of_week) +
                " %s" % CopticDateTime.from_time(time).day)

    def start(self, time):
        coptic_time = CopticDateTime.from_time(time)
        new_coptic = CopticDateTime.from_ymd(coptic_time.year, coptic_time.month, coptic_time.day)
        return new_coptic.to_time()

    def increment(self, time):
        return time + CopticDelta.from_days(1)

    def is_day(self):
        return True
