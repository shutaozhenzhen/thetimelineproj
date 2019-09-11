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


from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.calendar.pharaonic.time import PharaonicTime
from timelinelib.test.cases.unit import UnitTestCase


class describe_time_properties(UnitTestCase):

    def test_can_return_time_of_day(self):
        self.assertEqual((0, 0, 0), PharaonicTime(0, 0).get_time_of_day())
        self.assertEqual((0, 0, 1), PharaonicTime(0, 1).get_time_of_day())
        self.assertEqual((0, 1, 1), PharaonicTime(0, 61).get_time_of_day())
        self.assertEqual((2, 3, 5), PharaonicTime(0, 60 * 60 * 2 + 60 * 3 + 5).get_time_of_day())

    def test_add(self):
        self.assertEqual(PharaonicTime(10, 70), PharaonicTime(10, 61) + PharaonicDelta.from_seconds(9))
        self.assertEqual(PharaonicTime(11, 61), PharaonicTime(10, 61) + PharaonicDelta.from_days(1))

    def test_sub_delta(self):
        self.assertEqual(PharaonicTime(10, 60), PharaonicTime(10, 61) - PharaonicDelta.from_seconds(1))
        self.assertEqual(PharaonicTime(9, 24 * 60 * 60 - 1), PharaonicTime(10, 0) - PharaonicDelta.from_seconds(1))

    def test_sub_time(self):
        self.assertEqual(PharaonicDelta.from_seconds(5 * 24 * 60 * 60), PharaonicTime(10, 0) - PharaonicTime(5, 0))
        self.assertEqual(PharaonicDelta.from_seconds(5 * 24 * 60 * 60 + 5), PharaonicTime(10, 5) - PharaonicTime(5, 0))
        self.assertEqual(PharaonicDelta.from_seconds(4 * 24 * 60 * 60 + (24 * 60 * 60 - 5)), PharaonicTime(10, 5) - PharaonicTime(5, 10))

    def test_rejects_invalid_times(self):
        self.assertRaises(ValueError, PharaonicTime, PharaonicTime.MIN_JULIAN_DAY - 1, 0)
        self.assertRaises(ValueError, PharaonicTime, PharaonicTime.MIN_JULIAN_DAY, -1)
        self.assertRaises(ValueError, PharaonicTime, PharaonicTime.MIN_JULIAN_DAY, 24 * 60 * 60)

    #throws error because of main/source/timelinelibe/test/utils.py seems specific to the gregorian calendar
    """
    def test_can_be_compared(self):
        def a_time():
            return PharaonicTime(100, 100)
        self.assertEqNeImplementationIsCorrect(a_time, TIME_MODIFIERS)
    """

    def test_can_return_min_time(self):
        self.assertEqual(PharaonicTime(PharaonicTime.MIN_JULIAN_DAY, 0), PharaonicTime.min())


class describe_time_delta_properties(UnitTestCase):

    def test_can_create(self):
        self.assertEqual(PharaonicDelta.from_seconds(5), PharaonicDelta(5))
        self.assertEqual(PharaonicDelta.from_days(5), PharaonicDelta(5 * 24 * 60 * 60))

    def test_div(self):
        self.assertEqual(2.5, PharaonicDelta(5) / PharaonicDelta(2))

    def test_sub(self):
        self.assertEqual(PharaonicDelta(2) - PharaonicDelta(1), PharaonicDelta(1))

    def test_mul(self):
        self.assertEqual(PharaonicDelta(2), PharaonicDelta(5) * 0.5)
        self.assertEqual(PharaonicDelta(2), 0.5 * PharaonicDelta(5))

    def test_negate(self):
        self.assertEqual(PharaonicDelta(-2), -PharaonicDelta(2))

class desribe_pharaonic_time(UnitTestCase):

    def test_repr(self):
        self.assertEqual(
            repr(PharaonicTime(1, 2)),
            "PharaonicTime(1, 2)"
        )

    def test_str(self):
        self.assertEqual(
            str(PharaonicTime(1, 2)),
            "PharaonicTime(1, 2)"
        )

    def test_subtracting_gives_pharaonic_delta(self):
        self.assertIsInstance(
            PharaonicTime(1, 1) - PharaonicTime(1, 1),
            PharaonicDelta
        )

    def test_add(self):
        self.assertEqual(
            PharaonicTime(1, 1) + PharaonicDelta.from_seconds(1),
            PharaonicTime(1, 2)
        )

    def test_add_fail(self):
        self.assertRaises(TypeError, lambda: PharaonicTime(1, 1) + 4)

    def test_sub(self):
        self.assertEqual(
            PharaonicTime(1, 1) - PharaonicDelta.from_seconds(1),
            PharaonicTime(1, 0)
        )


class desribe_pharaonic_delta(UnitTestCase):

    def test_repr(self):
        self.assertEqual(
            repr(PharaonicDelta(5)),
            "PharaonicDelta(5)"
        )

    def test_str(self):
        self.assertEqual(
            str(PharaonicDelta(5)),
            "PharaonicDelta(5)"
        )

    def test_dividing_gives_pharaonic_delta(self):
        self.assertIsInstance(
            PharaonicDelta(4) / 2,
            PharaonicDelta
        )

    def test_dividing_gives_pharaonic_delta(self):
        self.assertIsInstance(
            PharaonicDelta(4) - PharaonicDelta(2),
            PharaonicDelta
        )

    def test_multiplying_gives_pharaonic_delta(self):
        self.assertIsInstance(
            PharaonicDelta(4) * 2,
            PharaonicDelta
        )
