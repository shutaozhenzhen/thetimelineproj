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
from timelinelib.calendar.gregorian.timetype import StripDecade
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian


class describe_gregorian_strip_decade(UnitTestCase):

    def test_label(self):
        for (time, expected_label) in [
            ("7 Jul -19", "20s ⟪BC⟫"),
            ("7 Jul -18", "10s ⟪BC⟫"),
            ("7 Jul -9", "10s ⟪BC⟫"),
            ("7 Jul -8", "0s ⟪BC⟫"),
            ("7 Jul 0", "0s ⟪BC⟫"),
            ("7 Jul 1", "0s"),
            ("7 Jul 9", "0s"),
            ("7 Jul 10", "10s"),
            ("7 Jul 19", "10s"),
            ("7 Jul 20", "20s"),
            ("7 Jul 2013", "2010s"),
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


