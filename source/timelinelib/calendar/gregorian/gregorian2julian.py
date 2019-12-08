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


def gregorian_ymd_to_julian_day(year, month, day):
    """
    This algorithm is described here:

    * http://www.tondering.dk/claus/cal/julperiod.php#formula
    * http://en.wikipedia.org/wiki/Julian_day#Converting_Julian_or_Gregorian_calendar_date_to_Julian_Day_Number

    Integer division works differently in C and in Python for negative numbers.
    C truncates towards 0 and Python truncates towards negative infinity:
    http://python-history.blogspot.se/2010/08/why-pythons-integer-division-floors.html

    The above sources don't state which to be used. If we can prove that
    division-expressions are always positive, we can be sure this algorithm
    works the same in C and in Python.

    We must prove that:

    1) y >= 0
    2) ((153 * m) + 2) >= 0

    Let's prove 1):

    y = year + 4800 - a
      = year + 4800 - ((14 - month) // 12)

    year >= -4713 (gives a julian day of 0)

    so

    year + 4800 >= -4713 + 4800 = 87

    The expression ((14 - month) // 12) varies between 0 and 1 when month
    varies between 1 and 12. Therefore y >= 87 - 1 = 86, and 1) is proved.

    Let's prove 2):

    m = month + (12 * a) - 3
      = month + (12 * ((14 - month) // 12)) - 3

    1 <= month <= 12

    m(1)  = 1  + (12 * ((14 - 1)  // 12)) - 3 = 1  + (12 * 1) - 3 = 10
    m(2)  = 2  + (12 * ((14 - 2)  // 12)) - 3 = 2  + (12 * 1) - 3 = 11
    m(3)  = 3  + (12 * ((14 - 3)  // 12)) - 3 = 3  + (12 * 0) - 3 = 0
    m(4)  = 4  + (12 * ((14 - 4)  // 12)) - 3 = 4  + (12 * 0) - 3 = 1
    m(5)  = 5  + (12 * ((14 - 5)  // 12)) - 3 = 5  + (12 * 0) - 3 = 2
    m(6)  = 6  + (12 * ((14 - 6)  // 12)) - 3 = 6  + (12 * 0) - 3 = 3
    m(7)  = 7  + (12 * ((14 - 7)  // 12)) - 3 = 7  + (12 * 0) - 3 = 4
    m(8)  = 8  + (12 * ((14 - 8)  // 12)) - 3 = 8  + (12 * 0) - 3 = 5
    m(9)  = 9  + (12 * ((14 - 9)  // 12)) - 3 = 9  + (12 * 0) - 3 = 6
    m(10) = 10 + (12 * ((14 - 10) // 12)) - 3 = 10 + (12 * 0) - 3 = 7
    m(11) = 11 + (12 * ((14 - 11) // 12)) - 3 = 11 + (12 * 0) - 3 = 8
    m(12) = 12 + (12 * ((14 - 12) // 12)) - 3 = 12 + (12 * 0) - 3 = 9

    So, m is always > 0. Which also makes the expression ((153 * m) + 2) > 0,
    and 2) is proved.
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + (12 * a) - 3
    julian_day = (day
                  + (((153 * m) + 2) // 5)
                  + (y * 365)
                  + (y // 4)
                  - (y // 100)
                  + (y // 400)
                  - 32045)
    if julian_day < GregorianTime.MIN_JULIAN_DAY:
        raise ValueError("gregorian_ymd_to_julian_day only works for julian days >= %d, but was %d" % (
            GregorianTime.MIN_JULIAN_DAY, julian_day))
    return julian_day


def gregorian_ymd_to_julian_day_alt(year, month, day):
    """
    Table 15.14 Selected arithmetic calendars, with parameters for algorithms
        Calendar a         y   j   m  n  r   p    q  v   u    s  t  w  A  B       C

        1 Egyptian      3968   47  0 13  1   365  0  0   1   30  0  0
        2 Ethiopian     4720  124  0 13  4  1461  0  3   1   30  0  0
        3 Coptic        4996  124  0 13  4  1461  0  3   1   30  0  0
        4 Republican b  6504  111  0 13  4  1461  0  3   1   30  0  0 396 578797 −51
        5 Julian        4716 1401  2 12  4  1461  0  3   5  153  2  2
        6 Gregorian     4716 1401  2 12  4  1461  0  3   5  153  2  2 184 274277 −38
        7 Civil Islamic 5519 7664  0 12 30 10631 14 15 100 2951 51 10
        8 Baha’i ´ c    6560 1412 19 20  4  1461  0  3   1   19  0  0 184 274273 −50
        9 Saka          4794 1348  1 12  4  1461  0  3   1   31  0  0 184 274073 −36

    Algorithm 3. To convert a date D/M/Y in one of the calendars listed in Table 15.14 to a
                 Julian Day Number, J:
        1. h = M − m
        2. g = Y + y − (n − h)/n
        3. f = mod(h − 1+ n, n)
        4. e = (p ∗ g + q)/r + D − 1− j
        5. J = e + (s ∗ f + t)/u
        6. J = J − (3 ∗ ((g + A)/100))/4 − C

    """
    y = 4716
    j = 1401
    m = 2
    n = 12
    r = 4
    p = 1461
    q = 0
    v = 3
    u = 5
    s = 153
    t = 2
    w = 2
    A = 184
    B = 274277
    C = -38
    h = month - m
    g = year + y - (n - h) // n
    f = (h - 1 + n) % n
    e = (p * g + q) // r + day - 1 - j
    julian_day = e + (s * f + t) // u
    julian_day = julian_day - (3 * ((g + A) // 100)) // 4 - C
    return julian_day
