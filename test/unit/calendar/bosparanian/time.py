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


from timelinelib.calendar.bosparanian.time import BosparanianDelta
from timelinelib.calendar.bosparanian.time import BosparanianTime
from timelinelib.test.cases.unit import UnitTestCase


class desribe_bosparanian_time(UnitTestCase):

    def test_repr(self):
        self.assertEqual(
            repr(BosparanianTime(1, 2)),
            "BosparanianTime(1, 2)"
        )

    def test_str(self):
        self.assertEqual(
            str(BosparanianTime(1, 2)),
            "BosparanianTime(1, 2)"
        )

    def test_subtracting_gives_bosparanian_delta(self):
        self.assertIsInstance(
            BosparanianTime(1, 1) - BosparanianTime(1, 1),
            BosparanianDelta
        )

    def test_add(self):
        self.assertEqual(
            BosparanianTime(1, 1) + BosparanianDelta.from_seconds(1),
            BosparanianTime(1, 2)
        )

    def test_add_fail(self):
        self.assertRaises(TypeError, lambda: BosparanianTime(1, 1) + 4)

    def test_sub(self):
        self.assertEqual(
            BosparanianTime(1, 1) - BosparanianDelta.from_seconds(1),
            BosparanianTime(1, 0)
        )


class desribe_bosparanian_delta(UnitTestCase):

    def test_repr(self):
        self.assertEqual(
            repr(BosparanianDelta(5)),
            "BosparanianDelta(5)"
        )

    def test_str(self):
        self.assertEqual(
            str(BosparanianDelta(5)),
            "BosparanianDelta(5)"
        )

    def test_dividing_gives_bosparanian_delta(self):
        self.assertIsInstance(
            BosparanianDelta(4) / 2,
            BosparanianDelta
        )

    def test_dividing_gives_bosparanian_delta(self):
        self.assertIsInstance(
            BosparanianDelta(4) - BosparanianDelta(2),
            BosparanianDelta
        )

    def test_multiplying_gives_bosparanian_delta(self):
        self.assertIsInstance(
            BosparanianDelta(4) * 2,
            BosparanianDelta
        )
