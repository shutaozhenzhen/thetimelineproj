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

"""Unittest of class :doc:`Era <timelinelib_canvas_data_era>`."""

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.num.timetype import NumTimeType
from timelinelib.canvas.data.timeperiod import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_gregorian_era_with
from timelinelib.test.utils import a_numeric_era_with
from timelinelib.test.utils import ERA_MODIFIERS
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.test.utils import NUM_ERA_MODIFIERS
from timelinelib.test.utils import numeric_period


NAME = "Era name"
COLOR = (1, 2, 3)
GREGORIAN_START = "11 Jul 2014"
GREGORIAN_END = "11 Jul 2015"
NUM_START = 10
NUM_END = 20


class GregorianEraTestCase(UnitTestCase):
    """ """

    def setUp(self):
        """ """
        UnitTestCase.setUp(self)
        self.era = a_gregorian_era_with(name=NAME, color=COLOR, start=GREGORIAN_START, end=GREGORIAN_END)


class NumericEraTestCase(UnitTestCase):
    """ """

    def setUp(self):
        """ """
        UnitTestCase.setUp(self)
        self.era = a_numeric_era_with(name=NAME, color=COLOR, start=NUM_START, end=NUM_END)


class describe_gregorian_era_getters(GregorianEraTestCase):
    """ """

    def test_can_get_id(self):
        """ """
        self.assertEquals(None, self.era.get_id())
        self.assertFalse(self.era.has_id())

    def test_can_get_name(self):
        """ """
        self.assertEquals(NAME, self.era.get_name())

    def test_can_get_color(self):
        """ """
        self.assertEquals(COLOR, self.era.get_color())

    def test_can_get_time_period(self):
        """ """
        self.assertEquals(gregorian_period(GREGORIAN_START, GREGORIAN_END), self.era.get_time_period())


class describe_numeric_era_getters(NumericEraTestCase):
    """ """

    def test_can_get_id(self):
        """ """
        self.assertEquals(None, self.era.get_id())
        self.assertFalse(self.era.has_id())

    def test_can_get_name(self):
        """ """
        self.assertEquals(NAME, self.era.get_name())

    def test_can_get_color(self):
        """ """
        self.assertEquals(COLOR, self.era.get_color())

    def test_can_get_time_period(self):
        """ """
        self.assertEquals(numeric_period(NUM_START, NUM_END), self.era.get_time_period())


class describe_gregorian_era_setters(GregorianEraTestCase):
    """ """

    def test_can_set_id(self):
        """ """
        era_id = 100
        self.era.set_id(era_id)
        self.assertEquals(era_id, self.era.get_id())
        self.assertTrue(self.era.has_id())

    def test_can_set_name(self):
        """ """
        name = "New Era name"
        self.era.set_name(name)
        self.assertEquals(name, self.era.get_name())

    def test_can_set_color(self):
        """ """
        color = (122, 123, 124)
        self.era.set_color(color)
        self.assertEquals(color, self.era.get_color())

    def test_can_set_time_period(self):
        """ """
        start = "1 Aug 2010"
        end = "1 Aug 2011"
        period = gregorian_period(start, end)
        self.era.set_time_period(period)
        self.assertEquals(period, self.era.get_time_period())


class describe_numeric_era_setters(NumericEraTestCase):
    """ """

    def test_can_set_id(self):
        """ """
        era_id = 100
        self.era.set_id(era_id)
        self.assertEquals(era_id, self.era.get_id())
        self.assertTrue(self.era.has_id())

    def test_can_set_name(self):
        """ """
        name = "New Era name"
        self.era.set_name(name)
        self.assertEquals(name, self.era.get_name())

    def test_can_set_color(self):
        """ """
        color = (122, 123, 124)
        self.era.set_color(color)
        self.assertEquals(color, self.era.get_color())

    def test_can_set_time_period(self):
        """ """
        start = -50
        end = -10
        period = numeric_period(start, end)
        self.era.set_time_period(period)
        self.assertEquals(period, self.era.get_time_period())


class describe_gregorian_era_update(GregorianEraTestCase):
    """ """

    def test_can_update(self):
        """ """
        start = "9 Jan -10"
        end = "9 Jan -1"
        period = gregorian_period(start, end)
        name = "Updated name"
        color = (111, 110, 109)
        self.era.update(human_time_to_gregorian(start), human_time_to_gregorian(end), name, color)
        self.assertEquals(name, self.era.get_name())
        self.assertEquals(color, self.era.get_color())
        self.assertEquals(period, self.era.get_time_period())


class describe_numeric_era_update(NumericEraTestCase):
    """ """

    def test_can_update(self):
        """ """
        start = 100
        end = 200
        period = numeric_period(start, end)
        name = "Updated name"
        color = (111, 110, 109)
        self.era.update(start, end, name, color)
        self.assertEquals(name, self.era.get_name())
        self.assertEquals(color, self.era.get_color())
        self.assertEquals(period, self.era.get_time_period())


class describe_gregorian_era_comparision(NumericEraTestCase):
    """ """

    def test_can_be_compared(self):
        """ """
        self.assertEqNeImplementationIsCorrect(a_gregorian_era_with, ERA_MODIFIERS)


class describe_numeric_era_comparision(NumericEraTestCase):
    """ """

    def test_can_be_compared(self):
        """ """
        self.assertEqNeImplementationIsCorrect(a_numeric_era_with, NUM_ERA_MODIFIERS)


class describe_gregorian_era_features(GregorianEraTestCase):
    """ """

    def test_can_decide_period_overlapping(self):
        """ """
        period = gregorian_period(GREGORIAN_START, GREGORIAN_END)
        self.assertTrue(a_gregorian_era_with(start="1 Jul 2014", end="12 Jul 2014").inside_period(period))
        self.assertTrue(a_gregorian_era_with(start=GREGORIAN_START, end="12 Jul 2014").inside_period(period))
        self.assertFalse(a_gregorian_era_with(start="11 Jul 2000", end="11 Jul 2001").inside_period(period))


class describe_numeric_era_features(NumericEraTestCase):
    """ """

    def test_can_decide_period_overlapping(self):
        """ """
        period = numeric_period(NUM_START, NUM_END)
        self.assertTrue(a_numeric_era_with(start=1, end=15).inside_period(period))
        self.assertTrue(a_numeric_era_with(start=1, end=NUM_START).inside_period(period))
        self.assertFalse(a_numeric_era_with(start=1, end=5).inside_period(period))
