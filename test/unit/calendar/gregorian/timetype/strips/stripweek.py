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
from timelinelib.calendar.gregorian.timetype import StripWeek
from timelinelib.test.cases.wxapp import WxAppTestCase
from timelinelib.canvas.appearance import Appearance


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
            "7-13 ⟪Jul⟫ 2013"
        )

    def test_label_major_when_week_starts_on_monday(self):
        self.appearance.set_week_start("monday")
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00"), True),
            "⟪Week⟫ 27 (1-7 ⟪Jul⟫ 2013)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-4-07-07 00:00:00"), True),
            "⟪Week⟫ 27 (1-7 ⟪Jul⟫ 5 ⟪BC⟫)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-11-25 00:00:00"), True),
            "⟪Week⟫ 48 (25 ⟪Nov⟫-1 ⟪Dec⟫ 2013)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-4-11-25 00:00:00"), True),
            "⟪Week⟫ 48 (25 ⟪Nov⟫-1 ⟪Dec⟫ 5 ⟪BC⟫)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-12-30 00:00:00"), True),
            "⟪Week⟫ 1 (30 ⟪Dec⟫ 2013-5 ⟪Jan⟫ 2014)"
        )
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("-4-12-30 00:00:00"), True),
            "⟪Week⟫ 1 (30 ⟪Dec⟫ 5 ⟪BC⟫-5 ⟪Jan⟫ 4 ⟪BC⟫)"
        )

    def setUp(self):
        WxAppTestCase.setUp(self)
        self.time_type = GregorianTimeType()
        self.appearance = Appearance()
        self.strip = StripWeek(self.appearance)
