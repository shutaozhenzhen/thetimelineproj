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


from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.num.time import NumDelta
from timelinelib.calendar.num.time import NumTime
from timelinelib.calendar.num.timetype import move_period
from timelinelib.calendar.num.timetype import NumTimeType
from timelinelib.canvas.data import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase


class describe_numtimetype(UnitTestCase):

    def test_format_delta_1(self):
        self.assertEqual("1", NumTimeType().format_delta(NumDelta(1)))

    def test_format_delta_2(self):
        self.assertEqual("2", NumTimeType().format_delta(NumDelta(2)))

    def test_equality(self):
        self.assertEqual(NumTimeType(), NumTimeType())
        self.assertNotEqual(NumTimeType(), GregorianTimeType())


class decribe_num_time_duplicate_functions(UnitTestCase):

    def test_move_period_adds_given_number_of_delta(self):
        self.assertEqual(
            TimePeriod(NumTime(7), NumTime(8)),
            move_period(TimePeriod(NumTime(1), NumTime(2)), 6)
        )
