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


import datetime

import wx

from timelinelib.calendar.gregorian.time import GregorianTime
from timelinelib.test.cases.unit import UnitTestCase
import timelinelib.calendar.gregorian.gregorian as gregorian


class describe_gregorian(UnitTestCase):

    def test_rejects_invalid_dates(self):
        self.assertRaises(ValueError, gregorian.GregorianDateTime, 2013, 0, 1, 0, 0, 0)

    def test_can_replace(self):
        g = gregorian.GregorianDateTime(2013, 7, 12, 10, 16, 12)
        self.assertEqual(g.replace(year=1990), gregorian.GregorianDateTime(1990, 7, 12, 10, 16, 12))
        self.assertEqual(g.replace(month=6), gregorian.GregorianDateTime(2013, 6, 12, 10, 16, 12))
        self.assertEqual(g.replace(year=1990, month=6), gregorian.GregorianDateTime(1990, 6, 12, 10, 16, 12))
        self.assertRaises(ValueError, g.replace, month=13)


class GregorianConversionsSpec(UnitTestCase):

    def test_can_convert_from_timeline_time_to_gregorian(self):
        self.assertEqual(
            gregorian.GregorianDateTime.from_time(GregorianTime(julian_day=0, seconds=0)),
            gregorian.GregorianDateTime(-4713, 11, 24, 0, 0, 0))
        self.assertEqual(
            gregorian.GregorianDateTime.from_time(GregorianTime(julian_day=1, seconds=0)),
            gregorian.GregorianDateTime(-4713, 11, 25, 0, 0, 0))

    def test_can_convert_from_gregorian_to_timeline_time(self):
        self.assertEqual(
            gregorian.GregorianDateTime(-4713, 11, 24, 0, 0, 0).to_time(),
            GregorianTime(julian_day=0, seconds=0))
        self.assertEqual(
            gregorian.GregorianDateTime(-4713, 11, 25, 0, 0, 0).to_time(),
            GregorianTime(julian_day=1, seconds=0))

    def test_roundtrip_julian_day_conversions(self):
        for julian_day in range(100):
            (year, month, day) = gregorian.julian_day_to_gregorian_ymd(julian_day)
            roundtrip = gregorian.gregorian_ymd_to_julian_day(year, month, day)
            self.assertEqual(roundtrip, julian_day)

    def test_roundtrip_gregorian_dates_conversions(self):
        dates = [
            (2013, 1, 1),
            (2013, 1, 31),
        ]
        for gregorian_date in dates:
            (year, month, day) = gregorian_date
            julian_day = gregorian.gregorian_ymd_to_julian_day(year, month, day)
            roundtrip = gregorian.julian_day_to_gregorian_ymd(julian_day)
            self.assertEqual(roundtrip, gregorian_date)

    def test_works_same_as_python_date(self):
        py_date = datetime.date(1900, 1, 1)
        jd = gregorian.gregorian_ymd_to_julian_day(1900, 1, 1)
        for _ in range(365 * 200):
            (y, m, d) = gregorian.julian_day_to_gregorian_ymd(jd)
            self.assertEqual(py_date, datetime.date(y, m, d))
            py_date += datetime.timedelta(days=1)
            jd += 1

    def test_works_same_as_wx_date(self):
        STEP = 10000
        STOP = 10 * STEP
        for i in range(0, STOP, STEP):
            tm1 = GregorianTime(i, 0)
            gt = gregorian.GregorianDateTime.from_time(tm1)
            wt = wx.DateTime()
            wt.SetJDN(i)
            ws = "%d-%02d-%02d" % (wt.Year, wt.Month + 1, wt.Day)
            gs = "%d-%02d-%02d" % (gt.year, gt.month, gt.day)
            self.assertEqual(ws, gs)
            tm2 = gt.to_time()
            self.assertEqual(tm1, tm2)

    def test_new_to_julian_day(self):
        julian_day2 = gregorian.gregorian_ymd_to_julian_day_alt(2019, 06, 24)
        julian_day1 = gregorian.gregorian_ymd_to_julian_day(2019, 06, 24)
        self.assertEqual(julian_day1, julian_day2)


class describe_gregorian_primitives(UnitTestCase):

    def test_is_valid(self):
        self.assertTrue(gregorian.is_valid(2013, 1, 1))
        self.assertFalse(gregorian.is_valid(2013, 0, 1))
        self.assertFalse(gregorian.is_valid(2013, 13, 1))
        self.assertFalse(gregorian.is_valid(2013, 1, 0))
        self.assertFalse(gregorian.is_valid(2013, 1, 32))
        self.assertFalse(gregorian.is_valid(2013, 2, 30))

    def test_days_in_month(self):
        self.assertEqual(31, gregorian.days_in_month(2013, 1))
        self.assertEqual(28, gregorian.days_in_month(2013, 2))
        self.assertEqual(31, gregorian.days_in_month(2013, 3))
        self.assertEqual(30, gregorian.days_in_month(2013, 4))
        self.assertEqual(31, gregorian.days_in_month(2013, 5))
        self.assertEqual(30, gregorian.days_in_month(2013, 6))
        self.assertEqual(31, gregorian.days_in_month(2013, 7))
        self.assertEqual(31, gregorian.days_in_month(2013, 8))
        self.assertEqual(30, gregorian.days_in_month(2013, 9))
        self.assertEqual(31, gregorian.days_in_month(2013, 10))
        self.assertEqual(30, gregorian.days_in_month(2013, 11))
        self.assertEqual(31, gregorian.days_in_month(2013, 12))
        self.assertEqual(29, gregorian.days_in_month(2016, 2))

    def test_is_leap_year(self):
        self.assertFalse(gregorian.is_leap_year(2013))
        self.assertFalse(gregorian.is_leap_year(1900))
        self.assertTrue(gregorian.is_leap_year(2016))
        self.assertTrue(gregorian.is_leap_year(2000))

    def test_week_number(self):
        def assert_is_week(date_tuple, w):
            (y, m, d) = date_tuple
            date = gregorian.GregorianDateTime.from_ymd(y, m, d)
            self.assertEqual(date.week_number, w)
        assert_is_week((2012, 12, 30), 52)
        assert_is_week((2012, 12, 31), 1)
        assert_is_week((2013, 1, 1), 1)
        assert_is_week((2013, 1, 6), 1)
        assert_is_week((2013, 1, 7), 2)
        assert_is_week((2013, 7, 2), 27)

    def test_week_number_against_python(self):
        self.longMessage = True
        time = datetime.date(1900, 1, 1)
        for _ in range(365 * 50):
            y = time.year
            m = time.month
            d = time.day
            self.assertEqual(
                gregorian.GregorianDateTime.from_ymd(y, m, d).week_number,
                time.isocalendar()[1],
                "%s" % time
            )
            time += datetime.timedelta(days=1)
