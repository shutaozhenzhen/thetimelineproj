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


from timelinelib.calendar.num.time import NumDelta
from timelinelib.calendar.num.time import NumTime
from timelinelib.canvas.data.internaltime import Time
from timelinelib.canvas.data.internaltime import TimeDelta
from timelinelib.test.cases.unit import UnitTestCase


class TimeImplementationTestTemplate(object):

    # Sanity checks for test set up.

    def test_objects_are_unique(self):
        objects = [
            self.start,
            self.end,
            self.delta,
            self.delta_neg,
            self.double_delta,
        ]
        ids = [id(x) for x in objects]
        self.assertEqual(
            sorted(list(set(ids))),
            sorted(ids),
            "objects are not unique {0!r}".format(objects)
        )

    # Time == Time

    def test_time_eq_time(self):
        self.assertTrue(self.start == self.start)
        self.assertFalse(self.start == self.end)

    # Time != Time

    def test_time_ne_time(self):
        self.assertTrue(self.start != self.end)
        self.assertFalse(self.start != self.start)

    # Time < Time

    def test_time_lt_time(self):
        self.assertTrue(self.start < self.end)
        self.assertFalse(self.start < self.start)
        self.assertFalse(self.end < self.start)

    # Time <= Time

    def test_time_le_time(self):
        self.assertTrue(self.start <= self.end)
        self.assertTrue(self.start <= self.start)
        self.assertFalse(self.end <= self.start)

    # Time > Time

    def test_time_gt_time(self):
        self.assertTrue(self.end > self.start)
        self.assertFalse(self.end > self.end)
        self.assertFalse(self.start > self.end)

    # Time >= Time

    def test_time_ge_time(self):
        self.assertTrue(self.end >= self.start)
        self.assertTrue(self.end >= self.end)
        self.assertFalse(self.start >= self.end)

    # Delta == Delta

    def test_delta_eq_delta(self):
        self.assertTrue(self.delta == self.delta)
        self.assertFalse(self.delta == self.double_delta)

    # Delta != Delta

    def test_delta_ne_delta(self):
        self.assertTrue(self.delta != self.double_delta)
        self.assertFalse(self.delta != self.delta)

    # Delta < Delta

    def test_delta_lt_delta(self):
        self.assertTrue(self.delta < self.double_delta)
        self.assertFalse(self.delta < self.delta)
        self.assertFalse(self.double_delta < self.delta)

    # Delta <= Delta

    def test_delta_le_delta(self):
        self.assertTrue(self.delta <= self.double_delta)
        self.assertTrue(self.delta <= self.delta)
        self.assertFalse(self.double_delta <= self.delta)

    # Delta > Delta

    def test_delta_gt_delta(self):
        self.assertTrue(self.double_delta > self.delta)
        self.assertFalse(self.double_delta > self.double_delta)
        self.assertFalse(self.delta > self.double_delta)

    # Delta >= Delta

    def test_delta_ge_delta(self):
        self.assertTrue(self.double_delta >= self.delta)
        self.assertTrue(self.double_delta >= self.double_delta)
        self.assertFalse(self.delta >= self.double_delta)

    # Time + Delta

    def test_time_add_delta(self):
        self.assertEqual(self.start + self.delta, self.end)

    # Delta + Time

    def test_delta_add_time(self):
        self.assertEqual(self.delta + self.start, self.end)

    # Time - Time

    def test_time_sub_time(self):
        self.assertEqual(self.end - self.start, self.delta)

    # Time - Delta

    def test_time_sub_delta(self):
        self.assertEqual(self.end - self.delta, self.start)

    # Delta - Delta

    def test_delta_sub_delta(self):
        self.assertEqual(self.double_delta - self.delta, self.delta)

    # Delta * number

    def test_delta_mul_number(self):
        self.assertEqual(self.delta * 2, self.double_delta)

    # number * Delta

    def test_number_mul_delta(self):
        self.assertEqual(2 * self.delta, self.double_delta)

    # Delta / number

    def test_delta_div_number(self):
        self.assertEqual(self.double_delta / 2, self.delta)

    # Delta / Delta

    def test_delta_div_delta(self):
        self.assertEqual(self.delta / self.double_delta, 0.5)
        self.assertEqual(self.delta / self.delta_neg, -1)

    # -Delta

    def test_neg_delta(self):
        self.assertEqual(-self.delta, self.delta_neg)


class NumTimeTest(UnitTestCase, TimeImplementationTestTemplate):

    @property
    def start(self):
        return NumTime(1)

    @property
    def end(self):
        return NumTime(2)

    @property
    def delta(self):
        return NumDelta(1)

    @property
    def delta_neg(self):
        return NumDelta(-1)

    @property
    def double_delta(self):
        return NumDelta(2)


class InternalTimeTest(UnitTestCase, TimeImplementationTestTemplate):

    @property
    def start(self):
        return Time(1, 30)

    @property
    def end(self):
        return Time(2, 30)

    @property
    def delta(self):
        return TimeDelta(60*60*24)

    @property
    def delta_neg(self):
        return TimeDelta(-60*60*24)

    @property
    def double_delta(self):
        return TimeDelta(60*60*24*2)
