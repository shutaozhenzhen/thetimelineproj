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


class StripYear(Strip):

    def label(self, time, major=False):
        return format_year(BosparanianDateTime.from_time(time).year)

    def start(self, time):
        bosparanian_time = BosparanianDateTime.from_time(time)
        new_bosparanian = BosparanianDateTime.from_ymd(bosparanian_time.year, 1, 1)
        return new_bosparanian.to_time()

    def increment(self, time):
        bosparanian_time = BosparanianDateTime.from_time(time)
        return bosparanian_time.replace(year=bosparanian_time.year + 1).to_time()


def format_year(year):
    return f"{year}BF"


