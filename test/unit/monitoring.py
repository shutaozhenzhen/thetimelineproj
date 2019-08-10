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

"""Unittests of the class :doc:`Monitoring <timelinelib_monitoring>`."""

import sys
from timelinelib.test.cases.unit import UnitTestCase
from mock import Mock
from timelinelib.monitoring import Monitoring
from timelinelib.timer import Timer


class desribe_monitoring(UnitTestCase):
    """ """

    def test_counters_are_zero_at_start(self):
        """ """
        self.assertEquals(0, self.monitoring._timeline_redraw_count)
        self.assertEquals(0, self.monitoring._category_redraw_count)

    def test_timeline_redraw_counter_increments(self):
        """ """
        self.monitoring.count_timeline_redraw()
        self.assertEquals(1, self.monitoring._timeline_redraw_count)
        self.assertEquals(0, self.monitoring._category_redraw_count)

    def test_category_redraw_counter_increments(self):
        """ """
        self.monitoring.count_category_redraw()
        self.assertEquals(0, self.monitoring._timeline_redraw_count)
        self.assertEquals(1, self.monitoring._category_redraw_count)

    def test_returns_elapsed_time(self):
        """ """
        self.monitoring.timer_start()
        self.monitoring.timer_end()
        self.timer.start.assert_called_with()
        self.timer.end.assert_called_with()
        self.assertEquals(3, self.monitoring.timer_elapsed_ms)

    def setUp(self):
        self.timer = Mock(Timer)
        self.timer.elapsed_ms = 3
        self.monitoring = Monitoring(self.timer)
