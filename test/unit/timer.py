# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


import sys
import time

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.timer import Timer


class desribe_timer(UnitTestCase):

    def test_has_a_default_timer_on_windows(self):
        sys.platform = "win32"
        self.assertEquals(time.clock, Timer().default_timer)

    def test_has_a_default_timer_on_any_os(self):
        sys.platform = "any_os"
        self.assertEquals(time.time, Timer().default_timer)

    def test_can_start_timing(self):
        self.timer.start()
        self.assertEqual(1, self.counter)

    def test_can_stop_timing(self):
        self.timer.end()
        self.assertEqual(1, self.counter)

    def test_can_measure_elapsed_time(self):
        self.timer.start()
        self.timer.end()
        self.assertEqual(1000, self.timer.elapsed_ms)

    def setUp(self):
        self.counter = 0
        self.timer = Timer(self.timing)

    def timing(self):
        self.counter += 1
        return self.counter
