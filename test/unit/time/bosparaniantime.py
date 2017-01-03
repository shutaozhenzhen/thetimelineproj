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
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.time.bosparaniantime import BosparanianTimeType


class describe_bosparanian_time_type(UnitTestCase):

    def test_special_day(self):
        DAYS = [
            ("11 Jan 2016", False),
            ("12 Jan 2016", False),
            ("13 Jan 2016", False),
            ("14 Jan 2016", True), # Thursday
            ("15 Jan 2016", False),
            ("16 Jan 2016", False),
            ("17 Jan 2016", False),
        ]
        for day, expected_is_special in DAYS:
            self.assertEqual(
                self.time_type.is_special_day(human_time_to_gregorian(day)),
                expected_is_special
            )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = BosparanianTimeType()
