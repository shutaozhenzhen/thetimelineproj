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


from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.time.numtime import NumTimeType
from timelinelib.time.numtime import move_period
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.canvas.data import TimePeriod


class describe_numtimetype(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = NumTimeType()

    def test_returns_margin_delta(self):
        delta = 24 * 12345
        margin_delta = self.time_type.margin_delta(delta)
        self.assertEqual(12345, margin_delta)

    def test_format_delta_1(self):
        delta = 1
        self.assertEqual("1", self.time_type.format_delta(delta))

    def test_format_delta_2(self):
        delta = 2
        self.assertEqual("2", self.time_type.format_delta(delta))

    def test_equality(self):
        self.assertEqual(NumTimeType(), NumTimeType())
        self.assertNotEqual(NumTimeType(), GregorianTimeType())


class decribe_num_time_duplicate_functions(UnitTestCase):

    def setUp(self):
        self.period = TimePeriod(NumTimeType(), 1, 2)

    def test_move_period_adds_given_number_of_delta(self):
        new_period = move_period(self.period, 6)
        self.assertEqual(TimePeriod(NumTimeType(), 7, 8), new_period)
