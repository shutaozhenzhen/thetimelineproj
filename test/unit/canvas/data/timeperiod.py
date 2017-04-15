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


from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data.internaltime import Time
from timelinelib.canvas.data.internaltime import TimeDelta
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import TIME_PERIOD_MODIFIERS


class time_period_spec(UnitTestCase):

    def test_creating_period_with_end_before_start_should_fail(self):
        self.assertRaises(ValueError, TimePeriod, ATime(50), ATime(10))

    def test_inside_should_return_true_if_time_is_inside_period(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertTrue(tp.inside(ATime(3)))

    def test_inside_should_return_true_if_time_is_on_lower_edge(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertTrue(tp.inside(ATime(0)))

    def test_inside_should_return_true_if_time_is_on_higher_edge(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertTrue(tp.inside(ATime(4)))

    def test_inside_should_return_false_if_time_is_outside_period(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertFalse(tp.inside(ATime(5)))

    def test_delta_should_return_time_specific_delta(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertEqual(ADelta(4), tp.delta())

    def test_mean_time_should_return_time_specific_time(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertEqual(ATime(2), tp.mean_time())

    def test_center_should_center_period_around_time(self):
        tp = TimePeriod(ATime(0), ATime(4))
        self.assertEqual(
            tp.center(ATime(5)),
            TimePeriod(ATime(3), ATime(7)))

    def test_move_moves_1_10th_forward(self):
        time_period = TimePeriod(ATime(0), ATime(10))
        self.assertEqual(
            time_period.move(1),
            TimePeriod(ATime(1), ATime(11)))

    def test_move_moves_1_10th_backward(self):
        time_period = TimePeriod(ATime(20), ATime(30))
        self.assertEqual(
            time_period.move(-1),
            TimePeriod(ATime(19), ATime(29)))

    def test_zoom_in_removes_1_10th_on_each_side(self):
        time_period = TimePeriod(ATime(10), ATime(20))
        self.assertEqual(
            time_period.zoom(1),
            TimePeriod(ATime(11), ATime(19)))

    def test_zoom_out_adds_1_10th_on_each_side(self):
        time_period = TimePeriod(ATime(10), ATime(20))
        self.assertEqual(
            time_period.zoom(-1),
            TimePeriod(ATime(9), ATime(21)))

    def test_move_delta_moves_the_period_that_delta(self):
        time_period = TimePeriod(ATime(10), ATime(20))
        self.assertEqual(
            time_period.move_delta(ADelta(-10)),
            TimePeriod(ATime(0), ATime(10)))

    def test_can_be_compared(self):
        def a_time_period():
            return TimePeriod(ATime(50), ATime(60))
        self.assertEqNeImplementationIsCorrect(a_time_period, TIME_PERIOD_MODIFIERS)

    def test_overlaps(self):
        p = TimePeriod(ATime(10), ATime(20))
        self.assertFalse(p.overlaps(TimePeriod(ATime(0), ATime(9))))
        self.assertFalse(p.overlaps(TimePeriod(ATime(0), ATime(10))))
        self.assertTrue(p.overlaps(TimePeriod(ATime(0), ATime(11))))
        self.assertTrue(p.overlaps(TimePeriod(ATime(11), ATime(19))))
        self.assertTrue(p.overlaps(TimePeriod(ATime(19), ATime(30))))
        self.assertFalse(p.overlaps(TimePeriod(ATime(20), ATime(30))))
        self.assertFalse(p.overlaps(TimePeriod(ATime(21), ATime(30))))

    def test_inside_period(self):
        p = TimePeriod(ATime(10), ATime(20))
        self.assertFalse(p.inside_period(TimePeriod(ATime(0), ATime(9))))
        self.assertTrue(p.inside_period(TimePeriod(ATime(0), ATime(10))))
        self.assertTrue(p.inside_period(TimePeriod(ATime(0), ATime(11))))
        self.assertTrue(p.inside_period(TimePeriod(ATime(11), ATime(19))))
        self.assertTrue(p.inside_period(TimePeriod(ATime(19), ATime(30))))
        self.assertTrue(p.inside_period(TimePeriod(ATime(20), ATime(30))))
        self.assertFalse(p.inside_period(TimePeriod(ATime(21), ATime(30))))

    def test_get_time_at_percent(self):
        period_100 = TimePeriod(ATime(0), ATime(100))
        self.assertEqual(period_100.get_time_at_percent(0), ATime(0))
        self.assertEqual(period_100.get_time_at_percent(0.5), ATime(50))
        self.assertEqual(period_100.get_time_at_percent(1), ATime(100))


def ATime(num):
    return Time(num, 0)


def ADelta(num):
    return TimeDelta(num*60*60*24)
