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


from timelinelib.canvas.drawing.utils import Metrics
from timelinelib.data.timeperiod import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.time.numtime import NumTimeType


WIDTH = 200
HEIGHT = 100
START_TIME = human_time_to_gregorian("1 Jan 9988 00:00")
END_TIME = human_time_to_gregorian("1 Jan 9988 00:01")
START_NUM_TIME = 0
END_NUM_TIME = 1


class MetricsTestCase(UnitTestCase):

    def setUp(self):
        self.given_a_screen()

    def given_a_gregorian_scene_period(self, start_time=START_TIME, end_time=END_TIME):
        self.time_type = GregorianTimeType()
        self.time_period = TimePeriod(self.time_type, start_time, end_time)
        self.metrics = Metrics(self.screen_size, self.time_type, self.time_period, 50)

    def given_a_numeric_scene_period(self, start_time=START_NUM_TIME, end_time=END_NUM_TIME):
        self.time_type = NumTimeType()
        self.time_period = TimePeriod(self.time_type, start_time, end_time)
        self.metrics = Metrics(self.screen_size, self.time_type, self.time_period, 50)

    def given_a_screen(self, width=WIDTH, height=HEIGHT):
        self.screen_size = (width, height)


class describe_gregorian_overflow_error(MetricsTestCase):

    def test_x_is_zero_at_period_start(self):
        self.given_a_gregorian_scene_period()
        self.assertEquals(0, self.metrics.calc_x(START_TIME))

    def test_x_is_width_at_period_end(self):
        self.given_a_gregorian_scene_period()
        self.assertEquals(WIDTH, self.metrics.calc_x(END_TIME))

    def test_x_can_be_negative(self):
        self.given_a_gregorian_scene_period()
        time = human_time_to_gregorian("1 Jan -4700")
        self.assertTrue(self.metrics.calc_x(time) < 0)


class describe_numeric_overflow_error(MetricsTestCase):

    def test_x_is_zero_at_period_start(self):
        self.given_a_numeric_scene_period()
        self.assertEquals(0, self.metrics.calc_x(START_NUM_TIME))

    def test_x_is_width_at_period_end(self):
        self.given_a_numeric_scene_period()
        self.assertEquals(WIDTH, self.metrics.calc_x(END_NUM_TIME))

    def test_x_can_be_negative(self):
        self.given_a_numeric_scene_period()
        time = -10000
        self.assertTrue(self.metrics.calc_x(time) < 0)

    def test_negative_overflow_is_handled(self):
        self.given_a_numeric_scene_period()
        time = -1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        self.assertEquals(-1, self.metrics.calc_x(time))

    def test_positive_overflow_is_handled(self):
        self.given_a_numeric_scene_period()
        time = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        self.assertEquals(WIDTH + 1, self.metrics.calc_x(time))
