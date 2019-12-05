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


class StripDecade(Strip):

    def label(self, time, major=False):
        time = BosparanianDateTime.from_time(time)
        return format_decade(self._decade_start_year(time.year))

    def start(self, time):
        bosparanian_time = BosparanianDateTime.from_time(time)
        new_bosparanian = BosparanianDateTime.from_ymd(self._decade_start_year(bosparanian_time.year), 1, 1)
        return new_bosparanian.to_time()

    def increment(self, time):
        bosparanian_time = BosparanianDateTime.from_time(time)
        return bosparanian_time.replace(year=bosparanian_time.year + 10).to_time()

    @staticmethod
    def _decade_start_year(year):
        # The first start year must be to the left of the first visible
        # year on the timeline in order to draw the first vertical decade
        # line correctly. Therefore -10 in the calculation below
        return int(year // 10) * 10 - 10


def format_decade(start_year):
    return str(start_year + 10) + "s"


