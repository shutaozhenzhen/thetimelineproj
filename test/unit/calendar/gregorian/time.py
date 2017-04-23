# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


from timelinelib.calendar.gregorian.time import GregorianTime
from timelinelib.calendar.gregorian.time import GregorianTimeDelta
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import TIME_MODIFIERS


class describe_time_properties(UnitTestCase):

    def test_can_return_time_of_day(self):
        self.assertEqual((0, 0, 0), GregorianTime(0, 0).get_time_of_day())
        self.assertEqual((0, 0, 1), GregorianTime(0, 1).get_time_of_day())
        self.assertEqual((0, 1, 1), GregorianTime(0, 61).get_time_of_day())
        self.assertEqual((2, 3, 5), GregorianTime(0, 60 * 60 * 2 + 60 * 3 + 5).get_time_of_day())

    def test_add(self):
        self.assertEqual(GregorianTime(10, 70), GregorianTime(10, 61) + GregorianTimeDelta.from_seconds(9))
        self.assertEqual(GregorianTime(11, 61), GregorianTime(10, 61) + GregorianTimeDelta.from_days(1))

    def test_sub_delta(self):
        self.assertEqual(GregorianTime(10, 60), GregorianTime(10, 61) - GregorianTimeDelta.from_seconds(1))
        self.assertEqual(GregorianTime(9, 24 * 60 * 60 - 1), GregorianTime(10, 0) - GregorianTimeDelta.from_seconds(1))

    def test_sub_time(self):
        self.assertEqual(GregorianTimeDelta.from_seconds(5 * 24 * 60 * 60), GregorianTime(10, 0) - GregorianTime(5, 0))
        self.assertEqual(GregorianTimeDelta.from_seconds(5 * 24 * 60 * 60 + 5), GregorianTime(10, 5) - GregorianTime(5, 0))
        self.assertEqual(GregorianTimeDelta.from_seconds(4 * 24 * 60 * 60 + (24 * 60 * 60 - 5)), GregorianTime(10, 5) - GregorianTime(5, 10))

    def test_rejects_invalid_times(self):
        self.assertRaises(ValueError, GregorianTime, GregorianTime.MIN_JULIAN_DAY - 1, 0)
        self.assertRaises(ValueError, GregorianTime, GregorianTime.MIN_JULIAN_DAY, -1)
        self.assertRaises(ValueError, GregorianTime, GregorianTime.MIN_JULIAN_DAY, 24 * 60 * 60)

    def test_can_be_compared(self):
        def a_time():
            return GregorianTime(100, 100)
        self.assertEqNeImplementationIsCorrect(a_time, TIME_MODIFIERS)

    def test_can_return_min_time(self):
        self.assertEqual(GregorianTime(GregorianTime.MIN_JULIAN_DAY, 0), GregorianTime.min())


class describe_time_delta_properties(UnitTestCase):

    def test_can_create(self):
        self.assertEqual(GregorianTimeDelta.from_seconds(5), GregorianTimeDelta(5))
        self.assertEqual(GregorianTimeDelta.from_days(5), GregorianTimeDelta(5 * 24 * 60 * 60))

    def test_div(self):
        self.assertEqual(2.5, GregorianTimeDelta(5) / GregorianTimeDelta(2))

    def test_sub(self):
        self.assertEqual(GregorianTimeDelta(2) - GregorianTimeDelta(1), GregorianTimeDelta(1))

    def test_mul(self):
        self.assertEqual(GregorianTimeDelta(2), GregorianTimeDelta(5) * 0.5)
        self.assertEqual(GregorianTimeDelta(2), 0.5 * GregorianTimeDelta(5))

    def test_negate(self):
        self.assertEqual(GregorianTimeDelta(-2), -GregorianTimeDelta(2))
