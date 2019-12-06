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
from timelinelib.calendar.coptic.time import CopticTime
from timelinelib.canvas.drawing.interface import Strip
from timelinelib.calendar.coptic.timetype.formatters import format_year


class StripHour(Strip):

    def label(self, time, major=False):
        time = CopticDateTime.from_time(time)
        if major:
            return "%s %s %s: %sh" % (time.day, abbreviated_name_of_month(time.month),
                                      format_year(time.year), time.hour)
        return str(time.hour)

    def start(self, time):
        (hours, _, _) = time.get_time_of_day()
        return CopticTime(time.julian_day, hours * 60 * 60)

    def increment(self, time):
        return time + CopticDelta.from_seconds(60 * 60)
