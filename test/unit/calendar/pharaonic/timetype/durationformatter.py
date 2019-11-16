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
from timelinelib.calendar.pharaonic.timetype.timetype import DurationFormatter
from timelinelib.calendar.pharaonic.timetype.timetype import YEARS, MONTHS, DAYS, HOURS, MINUTES, SECONDS


Test = collections.namedtuple('Test', 'duration, expected_result')


class describe_duration_formatter(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)

    def test_formatting_all_possible_parts(self):
        tests = (
            Test(duration=[1, 1], expected_result='1 ⟪day⟫ 1 ⟪second⟫'),
            Test(duration=[1, 200], expected_result='1 ⟪day⟫ 3 ⟪minutes⟫ 20 ⟪seconds⟫'),
            Test(duration=[1, 40000], expected_result='1 ⟪day⟫ 11 ⟪hours⟫ 6 ⟪minutes⟫ 40 ⟪seconds⟫'),
            Test(duration=[400, 1], expected_result='1 ⟪year⟫ 1 ⟪month⟫ 5 ⟪days⟫ 1 ⟪second⟫'),
        )
        parts = (YEARS, MONTHS, DAYS, HOURS, MINUTES, SECONDS)
        for test in tests:
            self.assertEqual(test.expected_result, DurationFormatter(test.duration).format(parts))

    def test_formatting_years_and_days(self):
        tests = (
            Test(duration=[1, 1], expected_result='1 ⟪day⟫'),
            Test(duration=[2, 1], expected_result='2 ⟪days⟫'),
            Test(duration=[1, 200], expected_result='1 ⟪day⟫'),
            Test(duration=[1, 40000], expected_result='1 ⟪day⟫'),
            Test(duration=[400, 1], expected_result='1 ⟪year⟫ 35 ⟪days⟫'),
            Test(duration=[900, 1], expected_result='2 ⟪years⟫ 170 ⟪days⟫'),
        )
        parts = (YEARS, DAYS)
        for test in tests:
            self.assertEqual(test.expected_result, DurationFormatter(test.duration).format(parts))

    def test_formatting_seconds(self):
        tests = (
            Test(duration=[1, 1], expected_result='86401 ⟪seconds⟫'),
            Test(duration=[1, 200], expected_result='86600 ⟪seconds⟫'),
            Test(duration=[1, 40000], expected_result='126400 ⟪seconds⟫'),
            Test(duration=[400, 1], expected_result='34560001 ⟪seconds⟫'),
        )
        parts = (SECONDS,)
        for test in tests:
            self.assertEqual(test.expected_result, DurationFormatter(test.duration).format(parts))

    def test_formatting_months(self):
        tests = (
            Test(duration=[29, 0], expected_result=''),
            Test(duration=[30, 0], expected_result='1 ⟪month⟫'),
            Test(duration=[31, 0], expected_result='1 ⟪month⟫'),
            Test(duration=[59, 0], expected_result='1 ⟪month⟫'),
            Test(duration=[60, 0], expected_result='2 ⟪months⟫'),
        )
        parts = (MONTHS,)
        for test in tests:
            self.assertEqual(test.expected_result, DurationFormatter(test.duration).format(parts))

    def test_formatting_minutes(self):
        tests = (
            Test(duration=[0, 60], expected_result='1 ⟪minute⟫'),
            Test(duration=[0, 120], expected_result='2 ⟪minutes⟫'),
        )
        parts = (MINUTES,)
        for test in tests:
            self.assertEqual(test.expected_result, DurationFormatter(test.duration).format(parts))
