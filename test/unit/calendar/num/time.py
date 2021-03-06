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


from timelinelib.calendar.num.time import NumDelta
from timelinelib.calendar.num.time import NumTime
from timelinelib.test.cases.unit import UnitTestCase


class desribe_num_time(UnitTestCase):

    def test_repr(self):
        self.assertEqual(repr(NumTime(5)), "NumTime<5>")

    def test_str(self):
        self.assertEqual(str(NumTime(5)), "NumTime<5>")


class desribe_num_delta(UnitTestCase):

    def test_repr(self):
        self.assertEqual(repr(NumDelta(5)), "NumDelta<5>")

    def test_str(self):
        self.assertEqual(str(NumDelta(5)), "NumDelta<5>")
