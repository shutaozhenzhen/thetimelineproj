# -*- coding: utf-8 -*-
#
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


from timelinelib.calendar.coptic.time import CopticDelta
from timelinelib.calendar.coptic.timetype import CopticTimeType
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.coptic_utils import human_time_to_coptic


class describe_coptic_time_type(UnitTestCase):

    def test_is_weekend_day(self):
        DAYS = [
            ("9 II Shemu 1735", True), # Tkyriaka
            ("10 II Shemu 1735", False),
            ("11 II Shemu 1735", False),
            ("12 II Shemu 1735", False),
            ("13 II Shemu 1735", False),
            ("14 II Shemu 1735", False),
            ("15 II Shemu 1735", True), #Psabbaton
        ]
        for day, expected_is_weekend in DAYS:
            self.assertEqual(
                self.time_type.is_weekend_day(human_time_to_coptic(day)),
                expected_is_weekend
            )
            
    def test_format_delta(self):
        self.assertEqual(
            self.time_type.format_delta(CopticDelta.from_seconds(
                60*60 + 60 + 40
            )),
            u"1 ⟪hour⟫ 1 ⟪minute⟫ 40 ⟪seconds⟫"
        )
        self.assertEqual(
            self.time_type.format_delta(CopticDelta.from_days(366)),
            u"1 ⟪year⟫ 1 ⟪day⟫"
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.time_type = CopticTimeType()
