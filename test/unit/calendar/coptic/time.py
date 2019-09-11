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


from timelinelib.calendar.coptic.time import CopticDelta
from timelinelib.calendar.coptic.time import CopticTime
from timelinelib.test.cases.unit import UnitTestCase


class describe_time_properties(UnitTestCase):

    def test_can_return_time_of_day(self):
        self.assertEqual((0, 0, 0), CopticTime(0, 0).get_time_of_day())
        self.assertEqual((0, 0, 1), CopticTime(0, 1).get_time_of_day())
        self.assertEqual((0, 1, 1), CopticTime(0, 61).get_time_of_day())
        self.assertEqual((2, 3, 5), CopticTime(0, 60 * 60 * 2 + 60 * 3 + 5).get_time_of_day())

    def test_add(self):
        self.assertEqual(CopticTime(10, 70), CopticTime(10, 61) + CopticDelta.from_seconds(9))
        self.assertEqual(CopticTime(11, 61), CopticTime(10, 61) + CopticDelta.from_days(1))

    def test_sub_delta(self):
        self.assertEqual(CopticTime(10, 60), CopticTime(10, 61) - CopticDelta.from_seconds(1))
        self.assertEqual(CopticTime(9, 24 * 60 * 60 - 1), CopticTime(10, 0) - CopticDelta.from_seconds(1))

    def test_sub_time(self):
        self.assertEqual(CopticDelta.from_seconds(5 * 24 * 60 * 60), CopticTime(10, 0) - CopticTime(5, 0))
        self.assertEqual(CopticDelta.from_seconds(5 * 24 * 60 * 60 + 5), CopticTime(10, 5) - CopticTime(5, 0))
        self.assertEqual(CopticDelta.from_seconds(4 * 24 * 60 * 60 + (24 * 60 * 60 - 5)), CopticTime(10, 5) - CopticTime(5, 10))

    def test_rejects_invalid_times(self):
        self.assertRaises(ValueError, CopticTime, CopticTime.MIN_JULIAN_DAY - 1, 0)
        self.assertRaises(ValueError, CopticTime, CopticTime.MIN_JULIAN_DAY, -1)
        self.assertRaises(ValueError, CopticTime, CopticTime.MIN_JULIAN_DAY, 24 * 60 * 60)

    #throws error because of main/source/timelinelibe/test/utils.py seems specific to the gregorian calendar
    """
    def test_can_be_compared(self):
        def a_time():
            return CopticTime(100, 100)
        self.assertEqNeImplementationIsCorrect(a_time, TIME_MODIFIERS)
    """

    def test_can_return_min_time(self):
        self.assertEqual(CopticTime(CopticTime.MIN_JULIAN_DAY, 0), CopticTime.min())


class describe_time_delta_properties(UnitTestCase):

    def test_can_create(self):
        self.assertEqual(CopticDelta.from_seconds(5), CopticDelta(5))
        self.assertEqual(CopticDelta.from_days(5), CopticDelta(5 * 24 * 60 * 60))

    def test_div(self):
        self.assertEqual(2.5, CopticDelta(5) / CopticDelta(2))

    def test_sub(self):
        self.assertEqual(CopticDelta(2) - CopticDelta(1), CopticDelta(1))

    def test_mul(self):
        self.assertEqual(CopticDelta(2), CopticDelta(5) * 0.5)
        self.assertEqual(CopticDelta(2), 0.5 * CopticDelta(5))

    def test_negate(self):
        self.assertEqual(CopticDelta(-2), -CopticDelta(2))

class desribe_coptic_time(UnitTestCase):

    def test_repr(self):
        self.assertEqual(
            repr(CopticTime(1, 2)),
            "CopticTime(1, 2)"
        )

    def test_str(self):
        self.assertEqual(
            str(CopticTime(1, 2)),
            "CopticTime(1, 2)"
        )

    def test_subtracting_gives_coptic_delta(self):
        self.assertIsInstance(
            CopticTime(1, 1) - CopticTime(1, 1),
            CopticDelta
        )

    def test_add(self):
        self.assertEqual(
            CopticTime(1, 1) + CopticDelta.from_seconds(1),
            CopticTime(1, 2)
        )

    def test_add_fail(self):
        self.assertRaises(TypeError, lambda: CopticTime(1, 1) + 4)

    def test_sub(self):
        self.assertEqual(
            CopticTime(1, 1) - CopticDelta.from_seconds(1),
            CopticTime(1, 0)
        )


class desribe_coptic_delta(UnitTestCase):

    def test_repr(self):
        self.assertEqual(
            repr(CopticDelta(5)),
            "CopticDelta(5)"
        )

    def test_str(self):
        self.assertEqual(
            str(CopticDelta(5)),
            "CopticDelta(5)"
        )

    def test_dividing_gives_coptic_delta(self):
        self.assertIsInstance(
            CopticDelta(4) / 2,
            CopticDelta
        )

    def test_dividing_gives_coptic_delta(self):
        self.assertIsInstance(
            CopticDelta(4) - CopticDelta(2),
            CopticDelta
        )

    def test_multiplying_gives_coptic_delta(self):
        self.assertIsInstance(
            CopticDelta(4) * 2,
            CopticDelta
        )
