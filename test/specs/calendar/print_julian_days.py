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


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "source"))
    import __builtin__
    __builtin__.__dict__["_"] = lambda x: x
    from timelinelib.calendar.gregorian.gregorian import julian_day_to_gregorian_ymd
    from timelinelib.calendar.gregorian.gregorian import gregorian_ymd_to_julian_day
    for julian_day in range(10000000):
        (year, month, day) = julian_day_to_gregorian_ymd(julian_day)
        roundtrip_julian_day = gregorian_ymd_to_julian_day(year, month, day)
        print("%d - %d-%d-%d - %d" % (julian_day, year, month, day, roundtrip_julian_day))
