# -*- coding: utf-8 -*-
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

"""
Contains the GregorianDateTime class and static functions related
to the class.

:doc:`Tests are found here <unit_calendar_gregorian_gregorian>`.
"""


from timelinelib.calendar.gregorian.time import GregorianTime


def julian_day_to_gregorian_ymd(julian_day):
    """
    This algorithm is described here:

    * http://www.tondering.dk/claus/cal/julperiod.php#formula

    Integer division works differently in C and in Python for negative numbers.
    C truncates towards 0 and Python truncates towards negative infinity:
    http://python-history.blogspot.se/2010/08/why-pythons-integer-division-floors.html

    The above source don't state which to be used. If we can prove that
    division-expressions are always positive, we can be sure this algorithm
    works the same in C and in Python.

    We must prove that:

    1) m             >= 0
    2) ((5 * e) + 2) >= 0  =>  e >= 0
    3) (1461 * d)    >= 0  =>  d >= 0
    4) ((4 * c) + 3) >= 0  =>  c >= 0
    5) (b * 146097)  >= 0  =>  b >= 0
    6) ((4 * a) + 3) >= 0  =>  a >= 0

    Let's work from the top:

    julian_day >= 0                   =>

    a >= 0 + 32044
       = 32044                        =>

    This proves 6).

    b >= ((4 * 32044) + 3) // 146097
       = 0

    This proves 5).

    Let's look at c:

    c = a - ((b * 146097) // 4)
      = a - (((((4 * a) + 3) // 146097) * 146097) // 4)

    For c to be >= 0, then

    (((((4 * a) + 3) // 146097) * 146097) // 4) <= a

    Let's look at this component: ((((4 * a) + 3) // 146097) * 146097)

    This expression can never be larger than (4 * a) + 3. That gives this:

    ((4 * a) + 3) // 4 <= a, which holds.

    This proves 4).

    Now, let's look at d:

    d = ((4 * c) + 3) // 1461

    If c is >= 0, then d is also >= 0.

    This proves 3).

    Let's look at e:

    e = c - ((1461 * d) // 4)
      = c - ((1461 * (((4 * c) + 3) // 1461)) // 4)

    The same resoning as above can be used to conclude that e >= 0.

    This proves 2).

    Now, let's look at m:

    m = ((5 * e) + 2) // 153

    If e >= 0, then m is also >= 0.

    This proves 1).
    """
    if julian_day < GregorianTime.MIN_JULIAN_DAY:
        raise ValueError("julian_day_to_gregorian_ymd only works for julian days >= %d, but was %d" % (
            GregorianTime.MIN_JULIAN_DAY, julian_day))
    a = julian_day + 32044
    b = ((4 * a) + 3) // 146097
    c = a - ((b * 146097) // 4)
    d = ((4 * c) + 3) // 1461
    e = c - ((1461 * d) // 4)
    m = ((5 * e) + 2) // 153
    day = e - (((153 * m) + 2) // 5) + 1
    month = m + 3 - (12 * (m // 10))
    year = (b * 100) + d - 4800 + (m // 10)
    return year, month, day
