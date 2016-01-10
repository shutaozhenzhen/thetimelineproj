# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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


from timelinelib.time.timeline import Time
from timelinelib.time.timeline import BosparanianTime
from timelinelib.time.timeline import TimeDelta
from timelinelib.time.timeline import delta_from_seconds
from timelinelib.time.timeline import delta_from_days
from timelinelib.time.timeline import get_min_time
from timelinelib.time.timeline import MIN_JULIAN_DAY
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import TIME_MODIFIERS
from timelinelib.test.utils import human_time_to_gregorian


class describe_time_properties(UnitTestCase):

    def test_can_return_time_of_day(self):
        self.assertEqual((0, 0, 0), Time(0, 0).get_time_of_day())
        self.assertEqual((0, 0, 1), Time(0, 1).get_time_of_day())
        self.assertEqual((0, 1, 1), Time(0, 61).get_time_of_day())
        self.assertEqual((2, 3, 5), Time(0, 60 * 60 * 2 + 60 * 3 + 5).get_time_of_day())

    def test_add(self):
        self.assertEqual(Time(10, 70), Time(10, 61) + delta_from_seconds(9))
        self.assertEqual(Time(11, 61), Time(10, 61) + delta_from_days(1))

    def test_sub_delta(self):
        self.assertEqual(Time(10, 60), Time(10, 61) - delta_from_seconds(1))
        self.assertEqual(Time(9, 24 * 60 * 60 - 1), Time(10, 0) - delta_from_seconds(1))

    def test_sub_time(self):
        self.assertEqual(delta_from_seconds(5 * 24 * 60 * 60), Time(10, 0) - Time(5, 0))
        self.assertEqual(delta_from_seconds(5 * 24 * 60 * 60 + 5), Time(10, 5) - Time(5, 0))
        self.assertEqual(delta_from_seconds(4 * 24 * 60 * 60 + (24 * 60 * 60 - 5)), Time(10, 5) - Time(5, 10))

    def test_rejects_invalid_times(self):
        self.assertRaises(ValueError, Time, MIN_JULIAN_DAY - 1, 0)
        self.assertRaises(ValueError, Time, MIN_JULIAN_DAY, -1)
        self.assertRaises(ValueError, Time, MIN_JULIAN_DAY, 24 * 60 * 60)

    def test_can_be_compared(self):
        def a_time():
            return Time(100, 100)
        self.assertEqNeImplementationIsCorrect(a_time, TIME_MODIFIERS)

    def test_can_return_min_time(self):
        self.assertEqual(Time(MIN_JULIAN_DAY, 0), get_min_time())

    def test_is_weekend_day(self):
        self.assertFalse(human_time_to_gregorian("11 Jan 2016").is_weekend_day())  # Monday
        self.assertFalse(human_time_to_gregorian("12 Jan 2016").is_weekend_day())
        self.assertFalse(human_time_to_gregorian("13 Jan 2016").is_weekend_day())
        self.assertFalse(human_time_to_gregorian("14 Jan 2016").is_weekend_day())
        self.assertFalse(human_time_to_gregorian("15 Jan 2016").is_weekend_day())
        self.assertTrue(human_time_to_gregorian("16 Jan 2016").is_weekend_day())
        self.assertTrue(human_time_to_gregorian("17 Jan 2016").is_weekend_day())

    def test_is_special_day(self):
        for i in range(30):
            self.assertFalse(human_time_to_gregorian("%d Jan 2016" % (i + 1)).is_special_day())


class describe_time_delta_properties(UnitTestCase):

    def test_can_create(self):
        self.assertEqual(delta_from_seconds(5), TimeDelta(5))
        self.assertEqual(delta_from_days(5), TimeDelta(5 * 24 * 60 * 60))

    def test_div(self):
        self.assertEqual(2.5, TimeDelta(5) / TimeDelta(2))

    def test_sub(self):
        self.assertEqual(TimeDelta(2) - TimeDelta(1), TimeDelta(1))

    def test_mul(self):
        self.assertEqual(TimeDelta(2), TimeDelta(5) * 0.5)
        self.assertEqual(TimeDelta(2), 0.5 * TimeDelta(5))

    def test_negate(self):
        self.assertEqual(TimeDelta(-2), -TimeDelta(2))


class describe_bosparanian_time(UnitTestCase):

    def test_is_weekend_day(self):
        self.assertTrue(self.a_time("11 Jan 2016").is_weekend_day())  # Monday
        self.assertFalse(self.a_time("12 Jan 2016").is_weekend_day())
        self.assertFalse(self.a_time("13 Jan 2016").is_weekend_day())
        self.assertTrue(self.a_time("14 Jan 2016").is_weekend_day())  # Thursday
        self.assertFalse(self.a_time("15 Jan 2016").is_weekend_day())
        self.assertFalse(self.a_time("16 Jan 2016").is_weekend_day())
        self.assertFalse(self.a_time("17 Jan 2016").is_weekend_day())

    def test_is_special_day(self):
        self.assertFalse(self.a_time("11 Jan 2016").is_special_day())
        self.assertFalse(self.a_time("12 Jan 2016").is_special_day())
        self.assertFalse(self.a_time("13 Jan 2016").is_special_day())
        self.assertTrue(self.a_time("14 Jan 2016").is_special_day())  # Thursday
        self.assertFalse(self.a_time("15 Jan 2016").is_special_day())
        self.assertFalse(self.a_time("16 Jan 2016").is_special_day())
        self.assertFalse(self.a_time("17 Jan 2016").is_special_day())

    def a_time(self, time_spec):
        time = human_time_to_gregorian(time_spec)
        return BosparanianTime(time.julian_day, time.seconds)
