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


from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.calendar.pharaonic.timetype.timetype import PharaonicTimeType
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.pharaonic_utils import human_time_to_pharaonic


class describe_pharaonic_time_type(UnitTestCase):

    def test_is_weekend_day(self):
        DAYS = [
            ("1 I Akhet 1", False),
            ("2 II Akhet 18", False),
            ("3 I Peret 156", False),
            ("4 I Shemu -24", False),
            ("5 III Akhet 1654", False),
            ("6 III Shemu 784", False),
            ("7 II Peret 351", False),
            ("8 IV Peret -3000", False),
            ("9 II Shemu 1710", True),
            ("10 IV Akhet 99", True),
        ]
        for day, expected_is_weekend in DAYS:
            self.assertEqual(
                self.time_type.is_weekend_day(human_time_to_pharaonic(day)),
                expected_is_weekend
            )
            
    def test_format_delta(self):
        self.assertEqual(
            self.time_type.format_delta(PharaonicDelta.from_seconds(
                60*60 + 60 + 40
            )),
            "1 ⟪hour⟫ 1 ⟪minute⟫ 40 ⟪seconds⟫"
        )
        self.assertEqual(
            self.time_type.format_delta(PharaonicDelta.from_days(366)),
            "1 ⟪year⟫ 1 ⟪day⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = PharaonicTimeType()
