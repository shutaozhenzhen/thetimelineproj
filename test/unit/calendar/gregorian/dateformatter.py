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


from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.test.cases.unit import UnitTestCase


class describe_new_date_formatter(UnitTestCase):

    def test_can_format_and_parse_date(self):
        self.assert_format_parse((2016, 2, 13), ("2016-02-13", False))

    def test_can_format_and_parse_date_with_long_year(self):
        self.assert_format_parse((12345, 2, 13), ("12345-02-13", False))

    def test_can_format_and_parse_bc_date(self):
        self.assert_format_parse((-2015, 2, 13), ("2016-02-13", True))

    def test_can_format_and_parse_using_different_separators(self):
        self.formatter.set_separators("%", "*")
        self.assert_format_parse((2016, 2, 13), ("2016%02*13", False))

    def test_can_format_and_parse_with_different_ordering(self):
        self.formatter.set_region_order(year=1, month=0, day=2)
        self.assert_format_parse((2016, 2, 13), ("02-2016-13", False))

    def test_can_format_and_parse_with_month_name(self):
        self.formatter.use_abbreviated_name_for_month(True)
        self.assert_format_parse((2016, 2, 13), ("2016-#Feb#-13", False))

    def test_can_get_next_region(self):
        self.assert_next_region_is(("2016-02-13", 0), (5, 2))
        self.assert_next_region_is(("2016-02-13", 2), (5, 2))
        self.assert_next_region_is(("2016-02-13", 4), (5, 2))
        self.assert_next_region_is(("2016-02-13", 5), (8, 2))
        self.assert_next_region_is(("2016-02-13", 8), None)
        self.assert_next_region_is(("2016-02-13", 42), None)
        self.assert_next_region_is(("2016-02-", 8), None)
        self.assert_next_region_is(("2016-02", 7), None)
        self.assert_next_region_is(("", 0), None)
        self.assert_next_region_is(("2016-", 4), (5, 0))

    def test_can_get_previous_region(self):
        self.assert_previous_region_is(("2016-02-13", 42), (5, 2))
        self.assert_previous_region_is(("2016-02-13", 8), (5, 2))
        self.assert_previous_region_is(("2016-02-13", 7), (0, 4))
        self.assert_previous_region_is(("2016-02-13", 4), None)
        self.assert_previous_region_is(("2016-02-13", 0), None)

    def test_can_get_region_type(self):
        self.assert_region_type_is(("2016-02-13", 0), GregorianDateFormatter.YEAR)
        self.assert_region_type_is(("2016-02-13", 4), GregorianDateFormatter.YEAR)
        self.assert_region_type_is(("2016-02-13", 5), GregorianDateFormatter.MONTH)
        self.assert_region_type_is(("2016-02-13", 7), GregorianDateFormatter.MONTH)
        self.assert_region_type_is(("2016-02-13", 8), GregorianDateFormatter.DAY)

    def test_can_get_region_type_for_different_order(self):
        self.formatter.set_region_order(year=2, month=0, day=1)
        self.assert_region_type_is(("02-13-2015", 0), GregorianDateFormatter.MONTH)
        self.assert_region_type_is(("02-13-2015", 3), GregorianDateFormatter.DAY)
        self.assert_region_type_is(("02-13-2015", 6), GregorianDateFormatter.YEAR)

    def test_can_get_region_type_for_abbreviated_month_name(self):
        self.formatter.use_abbreviated_name_for_month(True)
        self.assert_region_type_is(("2015-#Feb#-10", 11), GregorianDateFormatter.DAY)

    def test_fails_if_region_order_is_incorrect(self):
        self.assertRaises(ValueError, self.formatter.set_region_order,
                          year=1, month=2, day=12)

    def test_fails_to_parse_if_date_is_invalid(self):
        self.assertRaises(ValueError, self.formatter.parse, ("20151211", False))
        self.assertRaises(ValueError, self.formatter.parse, ("2015-0-20", False))
        self.assertRaises(ValueError, self.formatter.parse, ("2015-13-20", False))
        self.assertRaises(ValueError, self.formatter.parse, ("2015-10-0", False))
        self.assertRaises(ValueError, self.formatter.parse, ("2015-02-29", False))

    def test_fails_if_trying_to_set_empty_separators(self):
        self.assertRaises(
            ValueError,
            self.formatter.set_separators, "", ""
        )

    def assert_format_parse(self, parsed, formatted):
        self.assertEqual(self.formatter.format(parsed), formatted)
        self.assertEqual(self.formatter.parse(formatted), parsed)

    def assert_next_region_is(self, current_position, expected_region):
        (date, cursor_position) = current_position
        self.assertEqual(
            self.formatter.get_next_region(date, cursor_position),
            expected_region
        )

    def assert_previous_region_is(self, current_position, expected_region):
        (date, cursor_position) = current_position
        self.assertEqual(
            self.formatter.get_previous_region(date, cursor_position),
            expected_region
        )

    def assert_region_type_is(self, current_position, expected_region_type):
        (date, cursor_position) = current_position
        self.assertEqual(
            self.formatter.get_region_type(date, cursor_position),
            expected_region_type
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.formatter = GregorianDateFormatter()
