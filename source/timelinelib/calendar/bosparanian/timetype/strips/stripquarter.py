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


class StripQuarter(Strip):

    def get_quarter(self, time):
        m = BosparanianDateTime.from_time(time).month
        if m == 13:
            return 0
        return (m - 1) // 3 + 1

    def label(self, time, major=False):
        q = self.get_quarter(time)
        if q == 0:
            return "NLD"
        return "Q%d" % q

    def start(self, time):
        q = self.get_quarter(time)
        if q == 0:
            m = 13
        else:
            m = (q - 1) * 3 + 1
        return BosparanianDateTime.from_ymd(BosparanianDateTime.from_time(time).year, m, 1).to_time()

    def increment(self, time):
        q = self.get_quarter(time)
        if q == 0:
            days_in_quarter = 5
        else:
            days_in_quarter = 30 * 3
        return time + BosparanianDelta.from_days(days_in_quarter)
