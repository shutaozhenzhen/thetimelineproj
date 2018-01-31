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


from timelinelib.test.cases.unit import UnitTestCase
import timelinelib.calendar.gregorian.monthnames


class MonthNamesSpec(UnitTestCase):

    def test_english_name_for_month_1_should_be_january(self):
        self.assertEqual(
            "January",
            timelinelib.calendar.gregorian.monthnames.english_name_of_month(1))

    def test_abbreviated_name_for_month_1_should_be_jan_translated(self):
        self.assertEqual(
            _("Jan"),
            timelinelib.calendar.gregorian.monthnames.abbreviated_name_of_month(1))

    def test_month_from_english_name_january_should_be_1(self):
        self.assertEqual(
            1,
            timelinelib.calendar.gregorian.monthnames.month_from_english_name("January"))

    def test_english_name_for_month_12_should_be_december(self):
        self.assertEqual(
            "December",
            timelinelib.calendar.gregorian.monthnames.english_name_of_month(12))

    def test_abbreviated_name_for_month_12_should_be_dec_translated(self):
        self.assertEqual(
            _("Dec"),
            timelinelib.calendar.gregorian.monthnames.abbreviated_name_of_month(12))

    def test_month_from_english_name_december_should_be_12(self):
        self.assertEqual(
            12,
            timelinelib.calendar.gregorian.monthnames.month_from_english_name("December"))
