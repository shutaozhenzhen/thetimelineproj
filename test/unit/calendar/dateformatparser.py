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


from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.calendar.dateformatparser import DateFormatParser
from timelinelib.calendar.dateformatparser import YEAR, MONTH, DAY


class describe_date_fromat_parser(UnitTestCase):

    def test_valid_parse_returns_separator_tuple(self):
        self.assertEqual(self.parser.parse("yyyy-mm/dd").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("yyyy-dd/mm").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("dd-yyyy/mm").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("dd-mm/yyyy").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("mm-yyyy/dd").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("mm-dd/yyyy").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("yyyy-mmm/dd").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("yyyy-dd/mmm").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("dd-yyyy/mmm").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("dd-mmm/yyyy").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("mmm-yyyy/dd").get_separators(), ("-", "/"))
        self.assertEqual(self.parser.parse("mmm-dd/yyyy").get_separators(), ("-", "/"))

    def test_parse_recognizes_muliple_char_separators(self):
        self.parser.parse("yyyy-mm-xx-dd")
        self.assertEqual(self.parser.get_separators(), ("-", "-xx-"))

    def test_parse_recognizes_month_names_format(self):
        self.parser.parse("yyyy-mmm-dd")
        self.assertEqual(self.parser.get_separators(), ("-", "-"))

    def test_valid_formats(self):
        formats = ("yyyy-mm-dd",
                   "yyyy-dd-mm",
                   "mm-yyyy-dd",
                   "mm-dd-yyyy",
                   "dd-yyyy-mm",
                   "dd-mm-yyyy",
                   "mm-dd-yyyy",
                   "dd-yyyy-mm",
                   "yyyy-dd-mm",
                   "dd-mm-yyyy",
                   "mm-yyyy-dd",
                   "yyyy-xx-mm-dd",
                   )
        for fmt in formats:
            self.assertTrue(self.parser.is_valid(fmt))

    def test_invalid_formats(self):
        formats = ("yyyy-mm",
                   "mm-dd-",
                   "xxxxxxxxxx",
                   "yyyy-xxxxx",
                   "yyyy-mm-xx",
                   "yyyy-mm-mm-dd",
                   "-yyyy-xx-mm-dd",
                   "yyyy-mm-dd-",
                   )
        for fmt in formats:
            self.assertFalse(self.parser.is_valid(fmt))

    def test_parse_regions(self):
        self.parser.parse("yyyy-mm-dd")
        self.assertEqual(self.parser.regions, [[0, 4, "", YEAR], [5, 2, "-", MONTH], [8, 2, "-", DAY]])

    def setUp(self):
        UnitTestCase.setUp(self)
        self.parser = DateFormatParser()
