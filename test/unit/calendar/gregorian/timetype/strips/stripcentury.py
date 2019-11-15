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
from timelinelib.calendar.gregorian.timetype import StripCentury
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian


class describe_gregorian_strip_century(UnitTestCase):

    def test_label_minor(self):
        self.assertEqual(
            self.strip.label(self.time_type.parse_time("2013-07-07 00:00:00")),
            "")

    def test_label_major(self):
        for (time, expected_label) in [
            ("7 Jul -199", "200s ⟪BC⟫"),
            ("7 Jul -198", "100s ⟪BC⟫"),
            ("7 Jul -99", "100s ⟪BC⟫"),
            ("7 Jul -98", "0s ⟪BC⟫"),
            ("7 Jul 0", "0s ⟪BC⟫"),
            ("7 Jul 1", "0s"),
            ("7 Jul 99", "0s"),
            ("7 Jul 100", "100s"),
            ("7 Jul 199", "100s"),
            ("7 Jul 200", "200s"),
            ("7 Jul 2013", "2000s"),
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
