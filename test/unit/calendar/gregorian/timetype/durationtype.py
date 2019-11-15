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


import collections

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.calendar.gregorian.timetype.durationtype import YEARS, MONTHS, WEEKS, DAYS, HOURS, MINUTES, SECONDS


class describe_duration_type(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)

    def test_years_duration(self):
        self.assertEqual(1, YEARS.value_fn((365, 0)))
        self.assertEqual((0, 0), YEARS.remainder_fn((365, 0)))

    def test_months_duration(self):
        self.assertEqual(1, MONTHS.value_fn((30, 0)))
        self.assertEqual((0, 0), MONTHS.remainder_fn((30, 0)))

    def test_weeks_duration(self):
        self.assertEqual(1, WEEKS.value_fn((7, 0)))
        self.assertEqual((0, 0), WEEKS.remainder_fn((7, 0)))

    def test_days_duration(self):
        self.assertEqual(1, DAYS.value_fn((1, 0)))
        self.assertEqual((0, 0), DAYS.remainder_fn((1, 0)))

    def test_hours_duration(self):
        self.assertEqual(1, HOURS.value_fn((0, 3600)))
        self.assertEqual((0, 0), HOURS.remainder_fn((1, 3600)))

    def test_minutes_duration(self):
        self.assertEqual(1, MINUTES.value_fn((0, 60)))
        self.assertEqual((0, 0), MINUTES.remainder_fn((1, 60)))
