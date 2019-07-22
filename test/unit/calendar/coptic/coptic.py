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

from timelinelib.calendar.coptic.time import CopticTime
from timelinelib.test.cases.unit import UnitTestCase
import timelinelib.calendar.coptic.coptic as coptic


class describe_coptic(UnitTestCase):

    def test_rejects_invalid_dates(self):
        self.assertRaises(ValueError, coptic.CopticDateTime, 2013, 0, 1, 0, 0, 0)

    def test_can_replace(self):
        g = coptic.CopticDateTime(2013, 7, 12, 10, 16, 12)
        self.assertEqual(g.replace(year=1990), coptic.CopticDateTime(1990, 7, 12, 10, 16, 12))
        self.assertEqual(g.replace(month=6), coptic.CopticDateTime(2013, 6, 12, 10, 16, 12))
        self.assertEqual(g.replace(year=1990, month=6), coptic.CopticDateTime(1990, 6, 12, 10, 16, 12))
        self.assertRaises(ValueError, g.replace, month=13)


class CopticConversionsSpec(UnitTestCase):

    def test_can_convert_from_timeline_time_to_coptic(self):
        self.assertEqual(
            coptic.CopticDateTime.from_time(CopticTime(julian_day=0, seconds=0)),
            coptic.CopticDateTime(-4996, 05, 05, 0, 0, 0))
        self.assertEqual(
            coptic.CopticDateTime.from_time(CopticTime(julian_day=1, seconds=0)),
            coptic.CopticDateTime(-4996, 05, 06, 0, 0, 0))

    def test_can_convert_from_coptic_to_timeline_time(self):
        self.assertEqual(
            coptic.CopticDateTime(-4996, 05, 05, 0, 0, 0).to_time(),
            CopticTime(julian_day=0, seconds=0))
        self.assertEqual(
            coptic.CopticDateTime(-4996, 05, 06, 0, 0, 0).to_time(),
            CopticTime(julian_day=1, seconds=0))

    def test_roundtrip_julian_day_conversions(self):
        for julian_day in range(100):
            (year, month, day) = coptic.julian_day_to_coptic_ymd(julian_day)
            roundtrip = coptic.coptic_ymd_to_julian_day(year, month, day)
            self.assertEqual(roundtrip, julian_day)

    def test_roundtrip_coptic_dates_conversions(self):
        dates = [
            (2013, 1, 1),
            (2013, 1, 30),
        ]
        for coptic_date in dates:
            (year, month, day) = coptic_date
            julian_day = coptic.coptic_ymd_to_julian_day(year, month, day)
            roundtrip = coptic.julian_day_to_coptic_ymd(julian_day)
            self.assertEqual(roundtrip, coptic_date)

class describe_coptic_primitives(UnitTestCase):

    def test_is_valid(self):
        self.assertTrue(coptic.is_valid(2013, 1, 1))
        self.assertFalse(coptic.is_valid(2013, 0, 1))
        self.assertFalse(coptic.is_valid(2013, 13, 7))
        self.assertFalse(coptic.is_valid(2013, 1, 0))
        self.assertFalse(coptic.is_valid(2013, 1, 32))
        self.assertFalse(coptic.is_valid(2013, 13, 6))

    def test_days_in_month(self):
        self.assertEqual(30, coptic.days_in_month(2013, 1))
        self.assertEqual(30, coptic.days_in_month(2013, 2))
        self.assertEqual(30, coptic.days_in_month(2013, 3))
        self.assertEqual(30, coptic.days_in_month(2013, 4))
        self.assertEqual(30, coptic.days_in_month(2013, 5))
        self.assertEqual(30, coptic.days_in_month(2013, 6))
        self.assertEqual(30, coptic.days_in_month(2013, 7))
        self.assertEqual(30, coptic.days_in_month(2013, 8))
        self.assertEqual(30, coptic.days_in_month(2013, 9))
        self.assertEqual(30, coptic.days_in_month(2013, 10))
        self.assertEqual(30, coptic.days_in_month(2013, 11))
        self.assertEqual(30, coptic.days_in_month(2013, 12))
        self.assertEqual(5, coptic.days_in_month(2014, 13))

    def test_is_leap_year(self):
        self.assertFalse(coptic.is_leap_year(2013))
        self.assertFalse(coptic.is_leap_year(1900))
        self.assertTrue(coptic.is_leap_year(2007))
        self.assertTrue(coptic.is_leap_year(1899))

    def test_week_number(self):
        def assert_is_week(date_tuple, w):
            (y, m, d) = date_tuple
            date = coptic.CopticDateTime.from_ymd(y, m, d)
            self.assertEqual(date.week_number, w)
            assert_is_week((1735, 1, 1), 1)
            assert_is_week((1735, 1, 5), 1)
            assert_is_week((1735, 1, 27), 5)
            assert_is_week((1734, 13, 4), 52)
            assert_is_week((1734, 13, 3), 51)
            assert_is_week((1735, 1, 1), 1)
            assert_is_week((1735, 7, 1), 27)
        """
            self.assertEqual(date.week_number, w)
        assert_is_week((2012, 12, 30), 36)
        assert_is_week((2012, 13, 1), 0)
        assert_is_week((2013, 1, 1), 1)
        assert_is_week((2013, 1, 10), 1)
        assert_is_week((2013, 1, 11), 2)
        assert_is_week((2013, 7, 2), 19)
        """
