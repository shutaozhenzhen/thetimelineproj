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
from timelinelib.calendar.gregorian.timetype import StripDay
from timelinelib.calendar.gregorian.timetype import StripHour
from timelinelib.calendar.gregorian.timetype import TimeOutOfRangeLeftError
from timelinelib.calendar.gregorian.timetype import TimeOutOfRangeRightError
from timelinelib.canvas.data import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
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
            "1 %s 2010 13:44 to 2 %s 2010 13:30" % (_("Aug"), _("Aug")),
            self.time_type.format_period(time_period))

    def test_returns_min_time(self):
        self.assertEqual(GregorianTime(0, 0), self.time_type.get_min_time())

    def test_returns_max_time(self):
        self.assertEqual(self.time_type.parse_time("9990-01-01 00:00:00"),
                         self.time_type.get_max_time())

    def test_get_weekday(self):
        dt = self.time_type.parse_time("2013-07-10 00:00:00")
        self.assertEqual(2, dt.day_of_week)

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
            t = human_time_to_gregorian(day)
            self.assertEqual(
                self.time_type.is_weekend_day(human_time_to_gregorian(day)),
                expected_is_weekend
            )


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
        self.assertEqual("1 %s" % _("day"), self.time_type.format_delta(delta))

    def test_format_one_minute_delta(self):
        delta = self.get_days_delta(days=0, hours=0, minutes=1)
        self.assertEqual("1 %s" % _("minute"), self.time_type.format_delta(delta))

    def test_format_two_minutes_delta(self):
        delta = self.get_days_delta(days=0, hours=0, minutes=2)
        self.assertEqual("2 %s" % _("minutes"), self.time_type.format_delta(delta))

    def test_format_one_hour_delta(self):
        delta = self.get_days_delta(days=0, hours=1, minutes=0)
        self.assertEqual("1 %s" % _("hour"), self.time_type.format_delta(delta))

    def test_format_two_hour_delta(self):
        delta = self.get_days_delta(days=0, hours=2, minutes=0)
        self.assertEqual("2 %s" % _("hours"), self.time_type.format_delta(delta))

    def test_format_one_day_delta(self):
        delta = self.get_days_delta(days=1, hours=0, minutes=0)
        self.assertEqual("1 %s" % _("day"), self.time_type.format_delta(delta))

    def test_format_two_days_delta(self):
        delta = self.get_days_delta(days=2, hours=0, minutes=0)
        self.assertEqual("2 %s" % _("days"), self.time_type.format_delta(delta))

    def test_format_one_hour_one_minute_delta(self):
        delta = self.get_days_delta(days=0, hours=1, minutes=1)
        self.assertEqual("1 %s 1 %s" % (_("hour"), _("minute")), self.time_type.format_delta(delta))

    def test_format_one_hour_two_minutes_delta(self):
        delta = self.get_days_delta(days=0, hours=1, minutes=2)
        self.assertEqual("1 %s 2 %s" % (_("hour"), _("minutes")), self.time_type.format_delta(delta))

    def test_format_one_day_one_hour_delta(self):
        delta = self.get_days_delta(days=1, hours=1, minutes=0)
        self.assertEqual("1 %s 1 %s" % (_("day"), _("hour")), self.time_type.format_delta(delta))

    def test_format_one_day_two_hour_delta(self):
        delta = self.get_days_delta(days=1, hours=2, minutes=0)
        self.assertEqual("1 %s 2 %s" % (_("day"), _("hours")), self.time_type.format_delta(delta))

    def test_format_two_days_two_hour_delta(self):
        delta = self.get_days_delta(days=2, hours=2, minutes=0)
        self.assertEqual("2 %s 2 %s" % (_("days"), _("hours")), self.time_type.format_delta(delta))

    def test_format_two_days_two_hour_one_minute_delta(self):
        delta = self.get_days_delta(days=2, hours=2, minutes=1)
        self.assertEqual("2 %s 2 %s 1 %s" % (_("days"), _("hours"), _("minute")), self.time_type.format_delta(delta))

    def test_format_two_days_two_hour_two_minutes_delta(self):
        delta = self.get_days_delta(days=2, hours=2, minutes=2)
        self.assertEqual("2 %s 2 %s 2 %s" % (_("days"), _("hours"), _("minutes")), self.time_type.format_delta(delta))

    def test_format_hundred_days_one_minute_delta(self):
        delta = self.get_days_delta(days=100, hours=0, minutes=0)
        self.assertEqual("100 %s" % _("days"), self.time_type.format_delta(delta))

    def test_format_2_years_2_months(self):
        time_period1 = self.create_point_period(1, 1, 1999, 0, 0)
        time_period2 = self.create_point_period(1, 3, 2001, 0, 0)
        delta = time_period2.start_time - time_period1.start_time
        self.assertEqual(
            '2 ⟪years⟫ 60 ⟪days⟫',
            self.time_type.format_delta(delta)
        )

    def test_format_overlapping_events(self):
        time_period1 = TimePeriod(self.time_type.parse_time("2010-08-01 13:44:00"),
                                  self.time_type.parse_time("2010-08-03 13:44:00"))
        time_period2 = TimePeriod(self.time_type.parse_time("2010-08-01 13:44:00"),
                                  self.time_type.parse_time("2010-08-03 13:44:00"))
        delta = time_period2.start_time - time_period1.end_time
        self.assertEqual(
            '2 ⟪days⟫',
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
