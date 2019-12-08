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

from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.time import GregorianTime


class GregorianDateTime:
    """ """

    def __init__(self, year, month, day, hour, minute, second):
        """ """
        if not is_valid(year, month, day):
            raise ValueError("Invalid gregorian date %s-%s-%s" % (year, month, day))
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __eq__(self, other):
        """ """
        return (isinstance(other, self.__class__) and self.to_tuple() == other.to_tuple())

    def __ne__(self, other):
        """ """
        return not (self == other)

    @classmethod
    def from_ymd(cls, year, month, day):
        """ """
        return cls(year, month, day, 0, 0, 0)

    @classmethod
    def from_time(cls, time):
        """ """
        (year, month, day) = julian_day_to_gregorian_ymd(time.julian_day)
        (hour, minute, second) = time.get_time_of_day()
        return cls(year, month, day, hour, minute, second)

    @property
    def week_number(self):
        """ """

        def monday_week_1(year):
            jan_4 = GregorianDateTime.from_ymd(year, 1, 4).to_time()
            return jan_4 - GregorianDelta.from_days(jan_4.day_of_week)

        def days_between(end, start):
            return end.julian_day - start.julian_day

        def days_since_monday_week_1(time):
            year = GregorianDateTime.from_time(time).year
            diff = days_between(end=time, start=monday_week_1(year + 1))
            if diff >= 0:
                return diff
            diff = days_between(end=time, start=monday_week_1(year))
            if diff >= 0:
                return diff
            diff = days_between(end=time, start=monday_week_1(year - 1))
            if diff >= 0:
                return diff
            raise ValueError("should not end up here")
        return days_since_monday_week_1(self.to_time()) // 7 + 1

    def is_bc(self):
        """ """
        return self.year <= 0

    def replace(self, year=None, month=None):
        """ """
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        return self.__class__(
            year,
            month,
            self.day,
            self.hour,
            self.minute,
            self.second
        )

    def days_in_month(self):
        """ """
        return days_in_month(self.year, self.month)

    def to_tuple(self):
        """ """
        return (self.year, self.month, self.day, self.hour, self.minute,
                self.second)

    def to_date_tuple(self):
        """ """
        return self.year, self.month, self.day

    def to_time_tuple(self):
        """ """
        return self.hour, self.minute, self.second

    def to_time(self):
        """ """
        days = gregorian_ymd_to_julian_day(self.year, self.month, self.day)
        seconds = self.hour * 60 * 60 + self.minute * 60 + self.second
        return GregorianTime(days, seconds)

    def is_first_day_in_year(self):
        """ """
        return (self.month == 1 and
                self.day == 1 and
                self.hour == 0 and
                self.minute == 0 and
                self.second == 0)

    def is_first_of_month(self):
        """ """
        return (self.day == 1 and
                self.hour == 0 and
                self.minute == 0 and
                self.second == 0)

    def __repr__(self):
        """ """
        return "GregorianDateTime<%d-%02d-%02d %02d:%02d:%02d>" % self.to_tuple()


def days_in_month(year, month):
    """ """
    if month in [4, 6, 9, 11]:
        return 30
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    if is_leap_year(year):
        return 29
    return 28


def is_leap_year(year):
    """ """
    return year % 4 == 0 and (year % 400 == 0 or not year % 100 == 0)


def is_valid_time(hour, minute, second):
    """ """
    return (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60)


def is_valid(year, month, day):
    """ """
    return (1 <= month <= 12 and 1 <= day <= days_in_month(year, month))


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
        raise ValueError("julian_day_to_gregorian_ymd only works for julian days >= %d, but was %d" % (GregorianTime.MIN_JULIAN_DAY, julian_day))
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
        raise ValueError("gregorian_ymd_to_julian_day only works for julian days >= %d, but was %d" % (GregorianTime.MIN_JULIAN_DAY, julian_day))
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
    f = (h -1 + n) % n
    e = (p * g + q) // r + day -1 - j
    julian_day = e + (s * f + t) // u
    julian_day = julian_day - (3 * ((g + A) // 100)) // 4 - C
    return julian_day
