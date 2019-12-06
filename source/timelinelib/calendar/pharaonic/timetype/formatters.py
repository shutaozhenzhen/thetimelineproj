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


from datetime import datetime
import re

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.pharaonic.pharaonic import PharaonicDateTime,\
    julian_day_to_pharaonic_ymd
from timelinelib.calendar.pharaonic.monthnames import abbreviated_name_of_month
from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.calendar.pharaonic.time import PharaonicTime
from timelinelib.calendar.pharaonic.time import SECONDS_IN_DAY
from timelinelib.calendar.pharaonic.weekdaynames import abbreviated_name_of_weekday
from timelinelib.calendar.timetype import TimeType
from timelinelib.canvas.data import TimeOutOfRangeLeftError
from timelinelib.canvas.data import TimeOutOfRangeRightError
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data import time_period_center
from timelinelib.canvas.drawing.interface import Strip
from timelinelib.calendar.gregorian.gregorian import gregorian_ymd_to_julian_day
from timelinelib.calendar.pharaonic.pharaonic import julian_day_to_pharaonic_ymd
from timelinelib.calendar.gregorian.timetype.durationformatter import DurationFormatter
from timelinelib.calendar.gregorian.timetype.durationtype import YEARS, DAYS, HOURS, MINUTES, SECONDS


BC = _("BC")


def format_year(year):
    if year <= 0:
        return "%d %s" % ((1 - year), BC)
    else:
        return str(year)


def get_day_of_week(time):
    return time.julian_day % 10
