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
from timelinelib.calendar.bosparanian.monthnames import bosp_name_of_month
from timelinelib.calendar.bosparanian.monthnames import bosp_abbreviated_name_of_month


class StripMonth(Strip):

    def label(self, time, major=False):
        time = BosparanianDateTime.from_time(time)
        if major:
            return "%s %s" % (bosp_name_of_month(time.month),
                              format_year(time.year))
        if time.month == 13:
            return bosp_abbreviated_name_of_month(time.month)
        return bosp_name_of_month(time.month)

    def start(self, time):
        bosparanian_time = BosparanianDateTime.from_time(time)
        new_bosparanian = BosparanianDateTime.from_ymd(bosparanian_time.year, bosparanian_time.month, 1)
        return new_bosparanian.to_time()

    def increment(self, time):
        days_in_month = BosparanianDateTime.from_time(time).days_in_month()
        return time + BosparanianDelta.from_days(days_in_month)
