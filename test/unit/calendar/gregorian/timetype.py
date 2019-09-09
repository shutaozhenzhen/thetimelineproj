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


import unittest.mock
import wx

from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.time import GregorianTime
from timelinelib.calendar.gregorian.timetype import backward_fn
from timelinelib.calendar.gregorian.timetype import backward_one_month_fn
from timelinelib.calendar.gregorian.timetype import backward_one_week_fn
from timelinelib.calendar.gregorian.timetype import backward_one_year_fn
from timelinelib.calendar.gregorian.timetype import fit_millennium_fn
from timelinelib.calendar.gregorian.timetype import fit_week_fn
from timelinelib.calendar.gregorian.timetype import forward_fn
from timelinelib.calendar.gregorian.timetype import forward_one_month_fn
from timelinelib.calendar.gregorian.timetype import forward_one_week_fn
from timelinelib.calendar.gregorian.timetype import forward_one_year_fn
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.gregorian.timetype import move_period_num_days
from timelinelib.calendar.gregorian.timetype import move_period_num_months
from timelinelib.calendar.gregorian.timetype import move_period_num_weeks
from timelinelib.calendar.gregorian.timetype import move_period_num_years
from timelinelib.calendar.gregorian.timetype import StripCentury
from timelinelib.calendar.gregorian.timetype import StripDay
from timelinelib.calendar.gregorian.timetype import StripDecade
from timelinelib.calendar.gregorian.timetype import StripHour
from timelinelib.calendar.gregorian.timetype import StripMonth
from timelinelib.calendar.gregorian.timetype import StripWeek
from timelinelib.calendar.gregorian.timetype import StripWeekday
from timelinelib.calendar.gregorian.timetype import StripYear
from timelinelib.calendar.gregorian.timetype import TimeOutOfRangeLeftError
from timelinelib.calendar.gregorian.timetype import TimeOutOfRangeRightError
from timelinelib.canvas.appearance import Appearance
from timelinelib.canvas.data import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.cases.wxapp import WxAppTestCase
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame


class describe_gregoriantimetype(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()

    def test_converts_time_to_string(self):
        self.assertEqual(
            "-4713-11-24 00:00:00",
            self.time_type.time_string(GregorianTime(julian_day=0, seconds=0)))

    def test_parses_time_from_string(self):
        self.assertEqual(
            GregorianTime(julian_day=0, seconds=0),
            self.time_type.parse_time("-4713-11-24 00:00:00"))

    def test_raises_ValueError_when_parsing_invalid_time(self):
        self.assertRaises(
            ValueError,
            self.time_type.parse_time, "2010-31-31 0:0:0")

    def test_raises_ValueError_when_parsing_badly_formatted_time(self):
        self.assertRaises(
            ValueError,
            self.time_type.parse_time, "2010-31-hello 0:0:0")

    def test_formats_period_to_string(self):
        time_period = TimePeriod(self.time_type.parse_time("2010-08-01 13:44:00"),
                                 self.time_type.parse_time("2010-08-02 13:30:00"))
        self.assertEqual(
            u"1 %s 2010 13:44 to 2 %s 2010 13:30" % (_("Aug"), _("Aug")),
            self.time_type.format_period(time_period))

    def test_returns_min_time(self):
        self.assertEqual(GregorianTime(0, 0), self.time_type.get_min_time())

    def test_returns_max_time(self):
        self.assertEqual(self.time_type.parse_time("9990-01-01 00:00:00"),
                         self.time_type.get_max_time())

    def test_get_weekday(self):
        dt = self.time_type.parse_time("2013-07-10 00:00:00")
        self.assertEqual(2, self.time_type.get_day_of_week(dt))

    def test_get_min_zoom_delta(self):
        self.assertEqual(GregorianDelta(60), self.time_type.get_min_zoom_delta()[0])

    def test_is_weekend_day(self):
        DAYS = [
            ("11 Jan 2016", False),  # Monday
            ("12 Jan 2016", False),
            ("13 Jan 2016", False),
            ("14 Jan 2016", False),
            ("15 Jan 2016", False),
            ("16 Jan 2016", True),
            ("17 Jan 2016", True),
        ]
        for day, expected_is_weekend in DAYS:
            self.assertEqual(
                self.time_type.is_weekend_day(human_time_to_gregorian(day)),
                expected_is_weekend
            )


class describe_gregorian_strip_week(WxAppTestCase):

    def test_start_when_week_starts_on_sunday(self):
        self.appearance.set_week_start("sunday")
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 11:00:00")),
            self.time_type.parse_time("2013-07-07 00:00:00"))

    def test_start_when_week_starts_on_monday(self):
        self.appearance.set_week_start("monday")
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 11:00:00")),
            self.time_type.parse_time("2013-07-08 00:00:00"))

    def test_increments_7_days(self):
        self.assertEqual(
            self.strip.increment(self.time_type.parse_time("2013-07-07 00:00:00")),
            self.time_type.parse_time("2013-07-14 00:00:00"))

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            "")

    def test_label_major_has_no_week_when_week_starts_on_sunday(self):
        self.appearance.set_week_start("sunday")
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            u"7-13 ⟪Jul⟫ 2013"
        )

    def test_label_major_when_week_starts_on_monday(self):
        self.appearance.set_week_start("monday")
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            u"⟪Week⟫ 27 (1-7 ⟪Jul⟫ 2013)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-4-07-07 00:00:00"), True),
            u"⟪Week⟫ 27 (1-7 ⟪Jul⟫ 5 ⟪BC⟫)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-11-25 00:00:00"), True),
            u"⟪Week⟫ 48 (25 ⟪Nov⟫-1 ⟪Dec⟫ 2013)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-4-11-25 00:00:00"), True),
            u"⟪Week⟫ 48 (25 ⟪Nov⟫-1 ⟪Dec⟫ 5 ⟪BC⟫)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-12-30 00:00:00"), True),
            u"⟪Week⟫ 1 (30 ⟪Dec⟫ 2013-5 ⟪Jan⟫ 2014)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-4-12-30 00:00:00"), True),
            u"⟪Week⟫ 1 (30 ⟪Dec⟫ 5 ⟪BC⟫-5 ⟪Jan⟫ 4 ⟪BC⟫)"
        )

    def setUp(self):
        WxAppTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.appearance = Appearance()
        self.strip = StripWeek(self.appearance)


class describe_gregorian_strip_weekday(UnitTestCase):

    def test_start(self):
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 12:13:14")),
            self.time_type.parse_time("2013-07-10 00:00:00"))

    def test_increment(self):
        self.assertEqual(
            self.strip.increment(self.time_type.parse_time("2013-07-07 00:00:00")),
            self.time_type.parse_time("2013-07-08 00:00:00"))

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            u"⟪Sun⟫ 7"
        )

    def test_label_major(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            u"⟪Sun⟫ 7 ⟪Jul⟫ 2013"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 00:00:00"), True),
            u"⟪Fri⟫ 7 ⟪Jul⟫ 6 ⟪BC⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripWeekday()


class describe_gregorian_strip_hour(UnitTestCase):

    def test_start(self):
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 12:13:14")),
            self.time_type.parse_time("2013-07-10 12:00:00"))

    def test_increment(self):
        self.assertEqual(
            self.strip.increment(self.time_type.parse_time("2013-07-07 12:00:00")),
            self.time_type.parse_time("2013-07-07 13:00:00"))

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 12:00:00")),
            "12")

    def test_label_major(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 12:00:00"), True),
            u"7 ⟪Jul⟫ 2013: 12h"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 12:00:00"), True),
            u"7 ⟪Jul⟫ 6 ⟪BC⟫: 12h"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripHour()


class describe_gregorian_strip_day(UnitTestCase):

    def test_start(self):
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 12:33:15")),
            self.time_type.parse_time("2013-07-10 00:00:00"))

    def test_increment(self):
        self.assertEqual(
            self.strip.increment(self.time_type.parse_time("2013-07-10 00:00:00")),
            self.time_type.parse_time("2013-07-11 00:00:00"))

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            "7")

    def test_label_major(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            u"7 ⟪Jul⟫ 2013"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 00:00:00"), True),
            u"7 ⟪Jul⟫ 6 ⟪BC⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripDay()


class describe_gregorian_strip_month(UnitTestCase):

    def test_start(self):
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 12:33:15")),
            self.time_type.parse_time("2013-07-01 00:00:00"))

    def test_increment(self):
        self.assertEqual(
            self.strip.increment(self.time_type.parse_time("2013-07-01 00:00:00")),
            self.time_type.parse_time("2013-08-01 00:00:00"))

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            _("Jul"))

    def test_label_major(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            u"⟪Jul⟫ 2013"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 00:00:00"), True),
            u"⟪Jul⟫ 6 ⟪BC⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripMonth()


class describe_gregorian_strip_year(UnitTestCase):

    def test_start(self):
        self.assertEqual(
            self.strip.start(self.time_type.parse_time("2013-07-10 12:33:15")),
            self.time_type.parse_time("2013-01-01 00:00:00"))

    def test_increment(self):
        self.assertEqual(
            self.strip.increment(self.time_type.parse_time("2013-01-01 00:00:00")),
            self.time_type.parse_time("2014-01-01 00:00:00"))

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            "2013")
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 00:00:00")),
            u"6 ⟪BC⟫"
        )

    def test_label_major(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            "2013")
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 00:00:00"), True),
            u"6 ⟪BC⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripYear()


class describe_gregorian_strip_decade(UnitTestCase):

    def test_label(self):
        for (time, expected_label) in [
            ("7 Jul -19", u"20s ⟪BC⟫"),
            ("7 Jul -18", u"10s ⟪BC⟫"),
            ("7 Jul -9", u"10s ⟪BC⟫"),
            ("7 Jul -8", u"0s ⟪BC⟫"),
            ("7 Jul 0", u"0s ⟪BC⟫"),
            ("7 Jul 1", u"0s"),
            ("7 Jul 9", u"0s"),
            ("7 Jul 10", u"10s"),
            ("7 Jul 19", u"10s"),
            ("7 Jul 20", u"20s"),
            ("7 Jul 2013", u"2010s"),
        ]:
            self.assertEqual(
                self.strip.label(human_time_to_gregorian(time)),
                expected_label
            )

    def test_start(self):
        for (start_year, expected_decade_start_year) in [
            # 20s BC
            (-19, -28),
            # 10s BC
            (-18, -18),
            (-9, -18),
            # 0s BC
            (-8, -8),
            (0, -8),
            # 0s
            (1, 1),
            (9, 1),
            # 10s
            (10, 10),
            (19, 10),
            # 20s
            (20, 20),
            # 2010s
            (2010, 2010),
            (2013, 2010),
        ]:
            self.assertEqual(
                self.strip.start(human_time_to_gregorian(
                    "10 Jul {0} 12:33:15".format(start_year)
                )),
                human_time_to_gregorian(
                    "1 Jan {0} 00:00:00".format(expected_decade_start_year)
                )
            )

    def test_increment(self):
        for (start_year, expected_next_start_year) in [
            (-28, -18),
            (-18, -8),
            (-8, 1),
            (1, 10),
            (10, 20),
            (2010, 2020),
        ]:
            self.assertEqual(
                self.strip.increment(human_time_to_gregorian(
                    "1 Jan {0}".format(start_year)
                )),
                human_time_to_gregorian(
                    "1 Jan {0}".format(expected_next_start_year)
                )
            )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripDecade()


class describe_gregorian_strip_century(UnitTestCase):

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            "")

    def test_label_major(self):
        for (time, expected_label) in [
            ("7 Jul -199", u"200s ⟪BC⟫"),
            ("7 Jul -198", u"100s ⟪BC⟫"),
            ("7 Jul -99", u"100s ⟪BC⟫"),
            ("7 Jul -98", u"0s ⟪BC⟫"),
            ("7 Jul 0", u"0s ⟪BC⟫"),
            ("7 Jul 1", u"0s"),
            ("7 Jul 99", u"0s"),
            ("7 Jul 100", u"100s"),
            ("7 Jul 199", u"100s"),
            ("7 Jul 200", u"200s"),
            ("7 Jul 2013", u"2000s"),
        ]:
            self.assertEqual(
                self.strip.label(human_time_to_gregorian(time), major=True),
                expected_label,
            )

    def test_start(self):
        for (start_year, expected_century_start_year) in [
            # 200s BC
            (-199, -298),
            # 100s BC
            (-198, -198),
            (-99, -198),
            # # 0s BC
            (-98, -98),
            (0, -98),
            # 0s
            (1, 1),
            (99, 1),
            # 100s
            (100, 100),
            (199, 100),
            # 200s
            (200, 200),
            # 2000s
            (2000, 2000),
            (2010, 2000),
            (2099, 2000),
        ]:
            self.assertEqual(
                self.strip.start(human_time_to_gregorian(
                    "10 Jul {0} 12:33:15".format(start_year)
                )),
                human_time_to_gregorian(
                    "1 Jan {0} 00:00:00".format(expected_century_start_year)
                )
            )

    def test_increment(self):
        for (start_year, expected_next_start_year) in [
            (-298, -198),
            (-198, -98),
            (-98, 1),
            (1, 100),
            (100, 200),
            (200, 300),
        ]:
            self.assertEqual(
                self.strip.increment(human_time_to_gregorian(
                    "1 Jan {0}".format(start_year)
                )),
                human_time_to_gregorian(
                    "1 Jan {0}".format(expected_next_start_year)
                )
            )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripCentury()


class describe_gregorian_time_type_delta_formatting(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()

    def test_format_delta_method(self):
        time_period1 = TimePeriod(self.time_type.parse_time("2010-08-01 13:44:00"),
                                  self.time_type.parse_time("2010-08-01 13:44:00"))
        time_period2 = TimePeriod(self.time_type.parse_time("2010-08-02 13:44:00"),
                                  self.time_type.parse_time("2010-08-02 13:44:00"))
        delta = time_period2.start_time - time_period1.start_time
        self.assertEqual(u"1 %s" % _("day"), self.time_type.format_delta(delta))

    def test_format_one_minute_delta(self):
        delta = self.get_days_delta(days=0, hours=0, minutes=1)
        self.assertEqual(u"1 %s" % _("minute"), self.time_type.format_delta(delta))

    def test_format_two_minutes_delta(self):
        delta = self.get_days_delta(days=0, hours=0, minutes=2)
        self.assertEqual(u"2 %s" % _("minutes"), self.time_type.format_delta(delta))

    def test_format_one_hour_delta(self):
        delta = self.get_days_delta(days=0, hours=1, minutes=0)
        self.assertEqual(u"1 %s" % _("hour"), self.time_type.format_delta(delta))

    def test_format_two_hour_delta(self):
        delta = self.get_days_delta(days=0, hours=2, minutes=0)
        self.assertEqual(u"2 %s" % _("hours"), self.time_type.format_delta(delta))

    def test_format_one_day_delta(self):
        delta = self.get_days_delta(days=1, hours=0, minutes=0)
        self.assertEqual(u"1 %s" % _("day"), self.time_type.format_delta(delta))

    def test_format_two_days_delta(self):
        delta = self.get_days_delta(days=2, hours=0, minutes=0)
        self.assertEqual(u"2 %s" % _("days"), self.time_type.format_delta(delta))

    def test_format_one_hour_one_minute_delta(self):
        delta = self.get_days_delta(days=0, hours=1, minutes=1)
        self.assertEqual(u"1 %s 1 %s" % (_("hour"), _("minute")), self.time_type.format_delta(delta))

    def test_format_one_hour_two_minutes_delta(self):
        delta = self.get_days_delta(days=0, hours=1, minutes=2)
        self.assertEqual(u"1 %s 2 %s" % (_("hour"), _("minutes")), self.time_type.format_delta(delta))

    def test_format_one_day_one_hour_delta(self):
        delta = self.get_days_delta(days=1, hours=1, minutes=0)
        self.assertEqual(u"1 %s 1 %s" % (_("day"), _("hour")), self.time_type.format_delta(delta))

    def test_format_one_day_two_hour_delta(self):
        delta = self.get_days_delta(days=1, hours=2, minutes=0)
        self.assertEqual(u"1 %s 2 %s" % (_("day"), _("hours")), self.time_type.format_delta(delta))

    def test_format_two_days_two_hour_delta(self):
        delta = self.get_days_delta(days=2, hours=2, minutes=0)
        self.assertEqual(u"2 %s 2 %s" % (_("days"), _("hours")), self.time_type.format_delta(delta))

    def test_format_two_days_two_hour_one_minute_delta(self):
        delta = self.get_days_delta(days=2, hours=2, minutes=1)
        self.assertEqual(u"2 %s 2 %s 1 %s" % (_("days"), _("hours"), _("minute")), self.time_type.format_delta(delta))

    def test_format_two_days_two_hour_two_minutes_delta(self):
        delta = self.get_days_delta(days=2, hours=2, minutes=2)
        self.assertEqual(u"2 %s 2 %s 2 %s" % (_("days"), _("hours"), _("minutes")), self.time_type.format_delta(delta))

    def test_format_hundred_days_one_minute_delta(self):
        delta = self.get_days_delta(days=100, hours=0, minutes=0)
        self.assertEqual(u"100 %s" % _("days"), self.time_type.format_delta(delta))

    def test_format_2_years_2_months(self):
        time_period1 = self.create_point_period(1, 1, 1999, 0, 0)
        time_period2 = self.create_point_period(1, 3, 2001, 0, 0)
        delta = time_period2.start_time - time_period1.start_time
        self.assertEqual(
            u'2 ⟪years⟫ 60 ⟪days⟫',
            self.time_type.format_delta(delta)
        )

    def test_format_overlapping_events(self):
        time_period1 = TimePeriod(self.time_type.parse_time("2010-08-01 13:44:00"),
                                  self.time_type.parse_time("2010-08-03 13:44:00"))
        time_period2 = TimePeriod(self.time_type.parse_time("2010-08-01 13:44:00"),
                                  self.time_type.parse_time("2010-08-03 13:44:00"))
        delta = time_period2.start_time - time_period1.end_time
        self.assertEqual(
            u'2 ⟪days⟫',
            self.time_type.format_delta(delta)
        )

    def create_point_period(self, day, month, year, hour, minute):
        dt = GregorianDateTime(year, month, day, hour, minute, 0).to_time()
        return TimePeriod(dt, dt)

    def get_days_delta(self, days=0, hours=0, minutes=0):
        return GregorianDelta(days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60)


class describe_gregorian_time_navigation_functions(UnitTestCase):

    def test_fit_week_should_display_the_week_of_the_day_that_is_in_the_center(self):
        self.when_navigating(fit_week_fn, "30 Oct 2012", "13 Nov 2012")
        self.then_period_becomes("5 Nov 2012", "12 Nov 2012")

    def test_fit_week_sunday_start_should_display_the_week_of_the_day_that_is_in_the_center(self):
        self.when_navigating(fit_week_fn, "30 Oct 2012", "13 Nov 2012", False)
        self.then_period_becomes("4 Nov 2012", "11 Nov 2012")

    def test_fit_first_millennium_should_display_the_millennium_that_is_in_the_center(self):
        self.when_navigating(fit_millennium_fn, "1 Jan -4712", "1 Feb -4712")
        self.then_period_becomes("1 Jan -4712", "1 Jan -3712")

    def test_fit_millennium_should_display_the_millennium_that_is_in_the_center(self):
        self.when_navigating(fit_millennium_fn, "1 Jan 2010", "2 Jan 2010")
        self.then_period_becomes("1 Jan 2000", "1 Jan 3000")

    def test_fit_last_millennium_should_display_the_millennium_that_is_in_the_center(self):
        self.when_navigating(fit_millennium_fn, "1 Jan 9989", "1 Jan 9990")
        self.then_period_becomes("1 Jan 8990", "1 Jan 9990")

    def test_move_page_smart_not_smart_forward(self):
        self.when_navigating(forward_fn, "1 Jan 2010", "5 Jan 2010")
        self.then_period_becomes("5 Jan 2010", "9 Jan 2010")

    def test_move_page_smart_not_smart_backward(self):
        self.when_navigating(backward_fn, "5 Jan 2010", "9 Jan 2010")
        self.then_period_becomes("1 Jan 2010", "5 Jan 2010")

    def test_move_page_smart_month_forward(self):
        self.when_navigating(forward_fn, "1 Jan 2010", "1 Feb 2010")
        self.then_period_becomes("1 Feb 2010", "1 Mar 2010")

    def test_move_page_smart_month_forward_beyond_limit(self):
        self.assert_navigation_raises(
            TimeOutOfRangeRightError, forward_fn, "1 Jan 9000", "1 Dec 9989")

    def test_move_page_smart_month_backward(self):
        self.when_navigating(backward_fn, "1 Feb 2010", "1 Mar 2010")
        self.then_period_becomes("1 Jan 2010", "1 Feb 2010")

    def test_move_page_smart_month_backward_beyond_limit(self):
        self.assert_navigation_raises(
            TimeOutOfRangeLeftError, backward_fn, "1 Jan -4712", "1 Dec -4711")

    def test_move_page_smart_month_over_year_boundry_backward(self):
        self.when_navigating(backward_fn, "1 Jan 2010", "1 Mar 2010")
        self.then_period_becomes("1 Nov 2009", "1 Jan 2010")

    def test_move_page_smart_year_forward(self):
        self.when_navigating(forward_fn, "1 Jan 2010", "1 Jan 2011")
        self.then_period_becomes("1 Jan 2011", "1 Jan 2012")

    def test_move_page_smart_year_forward_beyond_limit(self):
        self.assert_navigation_raises(
            TimeOutOfRangeRightError, forward_fn, "1 Jan 9000", "1 Jan 9989")

    def test_move_page_smart_year_backward(self):
        self.when_navigating(backward_fn, "1 Jan 2011", "1 Jan 2012")
        self.then_period_becomes("1 Jan 2010", "1 Jan 2011")

    def test_move_page_smart_year_backward_beyond_limit(self):
        self.assert_navigation_raises(
            TimeOutOfRangeLeftError, backward_fn, "1 Jan -4712", "1 Jan -4711")

    def test_move_year_forward(self):
        self.when_navigating(forward_one_year_fn, "1 Jan 2009", "1 Jan 2010")
        self.then_period_becomes("1 Jan 2010", "1 Jan 2011")

    def test_move_year_backward(self):
        self.when_navigating(backward_one_year_fn, "1 Jan 2010", "1 Jan 2011")
        self.then_period_becomes("1 Jan 2009", "1 Jan 2010")

    def test_move_month_forward(self):
        self.when_navigating(forward_one_month_fn, "1 Jul 2009", "1 Aug 2009")
        self.then_period_becomes("1 Aug 2009", "1 Sep 2009")

    def test_move_month_backward(self):
        self.when_navigating(backward_one_month_fn, "1 Aug 2009", "1 Sep 2009")
        self.then_period_becomes("1 Jul 2009", "1 Aug 2009")

    def test_move_week_forward(self):
        self.when_navigating(forward_one_week_fn, "1 Jul 2009", "1 Aug 2009")
        self.then_period_becomes("8 Jul 2009", "8 Aug 2009")

    def test_move_week_backward(self):
        self.when_navigating(backward_one_week_fn, "8 Jul 2009", "8 Aug 2009")
        self.then_period_becomes("1 Jul 2009", "1 Aug 2009")

    def assert_navigation_raises(self, exception, fn, start, end):
        def navigation_fn(fn):
            self.assertRaises(exception, fn, self.time_period)
        self.time_period = gregorian_period(start, end)
        fn(None, self.time_period, navigation_fn)

    def when_navigating(self, fn, start, end, week_starts_on_monday=True):
        def navigation_fn(fn):
            self.new_period = fn(self.time_period)
        self.time_period = gregorian_period(start, end)
        main_frame = unittest.mock.Mock(MainFrame)
        main_frame.week_starts_on_monday.return_value = week_starts_on_monday
        fn(main_frame, self.time_period, navigation_fn)

    def then_period_becomes(self, start, end):
        self.assertEqual(gregorian_period(start, end), self.new_period)


class describe_gregorian_time_duplicate_function(UnitTestCase):

    def test_move_period_num_days_adds_given_number_of_days(self):
        new_period = move_period_num_days(self.period, 6)
        self.assertEqual(
            TimePeriod(
                GregorianDateTime(2010, 1, 7, 12, 0, 0).to_time(),
                GregorianDateTime(2010, 1, 7, 13, 0, 0).to_time()),
            new_period)

    def test_move_period_num_weeks_adds_given_number_of_weeks(self):
        new_period = move_period_num_weeks(self.period, -3)
        self.assertEqual(
            TimePeriod(
                GregorianDateTime(2009, 12, 11, 12, 0, 0).to_time(),
                GregorianDateTime(2009, 12, 11, 13, 0, 0).to_time()),
            new_period)

    def test_move_period_num_months_adds_given_number_of_months(self):
        new_period = move_period_num_months(self.period, 2)
        self.assertEqual(
            TimePeriod(
                GregorianDateTime(2010, 3, 1, 12, 0, 0).to_time(),
                GregorianDateTime(2010, 3, 1, 13, 0, 0).to_time()),
            new_period)

    def test_move_period_num_months_can_handle_year_boundries_up(self):
        new_period = move_period_num_months(self.period, 20)
        self.assertEqual(
            TimePeriod(
                GregorianDateTime(2011, 9, 1, 12, 0, 0).to_time(),
                GregorianDateTime(2011, 9, 1, 13, 0, 0).to_time()),
            new_period)

    def test_move_period_num_months_can_handle_year_boundries_down(self):
        new_period = move_period_num_months(self.period, -1)
        self.assertEqual(
            TimePeriod(
                GregorianDateTime(2009, 12, 1, 12, 0, 0).to_time(),
                GregorianDateTime(2009, 12, 1, 13, 0, 0).to_time()),
            new_period)

    def test_move_period_num_months_returns_none_if_day_does_not_exist(self):
        self.period = TimePeriod(
            GregorianDateTime(2010, 1, 31, 12, 0, 0).to_time(),
            GregorianDateTime(2010, 1, 31, 13, 0, 0).to_time())
        new_period = move_period_num_months(self.period, 1)
        self.assertEqual(None, new_period)

    def test_move_period_works_if_period_is_whole_month_case_1(self):
        self.assertPeriodsEqual(
            gregorian_period("1 Feb 2010", "1 Mar 2010"),
            move_period_num_months(
                gregorian_period("1 Jan 2010", "1 Feb 2010"),
                1
            )
        )

    def test_move_period_works_if_period_is_whole_month_case_2(self):
        self.assertPeriodsEqual(
            gregorian_period("1 Dec 2015", "1 Jan 2016"),
            move_period_num_months(
                gregorian_period("1 Nov 2015", "1 Dec 2015"),
                1
            )
        )

    def test_move_period_works_if_period_is_whole_year(self):
        self.assertPeriodsEqual(
            gregorian_period("1 Feb 2010", "1 Feb 2011"),
            move_period_num_months(
                gregorian_period("1 Jan 2010", "1 Jan 2011"),
                1
            )
        )

    def test_move_period_num_years_adds_given_number_of_years(self):
        new_period = move_period_num_years(self.period, 1)
        self.assertEqual(
            TimePeriod(
                GregorianDateTime(2011, 1, 1, 12, 0, 0).to_time(),
                GregorianDateTime(2011, 1, 1, 13, 0, 0).to_time()),
            new_period)

    def test_move_period_num_years_returns_none_if_year_does_not_exist(self):
        self.period = TimePeriod(
            GregorianDateTime(2012, 2, 29, 12, 0, 0).to_time(),
            GregorianDateTime(2012, 2, 29, 13, 0, 0).to_time())
        new_period = move_period_num_years(self.period, 1)
        self.assertEqual(None, new_period)

    def setUp(self):
        UnitTestCase.setUp(self)
        self.period = TimePeriod(
            GregorianDateTime(2010, 1, 1, 12, 0, 0).to_time(),
            GregorianDateTime(2010, 1, 1, 13, 0, 0).to_time())
