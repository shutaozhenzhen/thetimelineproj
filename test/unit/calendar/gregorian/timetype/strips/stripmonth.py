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


from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.gregorian.timetype import StripMonth
from timelinelib.test.cases.unit import UnitTestCase


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
            "⟪Jul⟫ 2013"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-5-07-07 00:00:00"), True),
            "⟪Jul⟫ 6 ⟪BC⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.strip = StripMonth()
