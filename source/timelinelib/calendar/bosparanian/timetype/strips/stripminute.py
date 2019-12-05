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
from timelinelib.calendar.bosparanian.time import BosparanianTime
from timelinelib.calendar.bosparanian.timetype.strips.stripyear import format_year
from timelinelib.calendar.bosparanian.monthnames import bosp_abbreviated_name_of_month


class StripMinute(Strip):

    def label(self, time, major=False):
        time = BosparanianDateTime.from_time(time)
        if major:
            return "%s %s %s: %s:%s" % (time.day, bosp_abbreviated_name_of_month(time.month),
                                        format_year(time.year), time.hour, time.minute)
        return str(time.minute)

    def start(self, time):
        (hours, minutes, _) = time.get_time_of_day()
        return BosparanianTime(time.julian_day, minutes * 60 + hours * 60 * 60)

    def increment(self, time):
        return time + BosparanianDelta.from_seconds(60)
