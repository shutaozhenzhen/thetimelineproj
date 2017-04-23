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


from mock import Mock
import wx

from timelinelib.calendar.gregorian.time import GregorianTime
from timelinelib.calendar.gregorian.time import GregorianTimeDelta
from timelinelib.calendar.timetype import TimeType
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas import TimelineCanvas
from timelinelib.canvas.timelinecanvascontroller import TimelineCanvasController
from timelinelib.test.cases.unit import UnitTestCase


class TimelineCanvasControllerTestCase(UnitTestCase):

    def setUp(self):
        self.setUpView()
        self.setUpDb()
        self.app = wx.App()
        self.drawer = Mock()
        self.controller = TimelineCanvasController(self.view, self.drawer)
        self.time_type = self.db.get_time_type()

    def setUpView(self):
        self.view = Mock(TimelineCanvas)
        self.view.GetDividerPosition.return_value = 0

    def setUpDb(self):
        self.db = MemoryDB()
        self.db.set_time_type(ATimeType())


class describe_navigate(TimelineCanvasControllerTestCase):

    def test_setting_period_works(self):
        self.controller.navigate(lambda tp: time_period(10, 11))
        self.assertEqual(self.controller.get_time_period(), time_period(10, 11))

    def test_setting_too_narrow_period_gives_error(self):
        self.assertNavigationFails(
            lambda tp: time_period(15, 15),
            r"Can't zoom deeper than"
        )

    def test_setting_too_left_period_gives_error(self):
        self.assertNavigationFails(
            lambda tp: time_period(0, 2),
            r"Can't scroll more to the left"
        )

    def test_setting_too_right_period_gives_error(self):
        self.assertNavigationFails(
            lambda tp: time_period(20, 21),
            r"Can't scroll more to the right"
        )

    def assertNavigationFails(self, navigate_fn, pattern):
        self.assertRaisesRegexp(
            ValueError,
            pattern,
            self.controller.navigate, navigate_fn
        )
        self.assertEqual(
            self.controller.get_time_period(),
            self.original_period
        )

    def setUp(self):
        TimelineCanvasControllerTestCase.setUp(self)
        self.controller.set_timeline(self.db)
        self.original_period = self.controller.get_time_period()


class ATimeType(TimeType):

    def get_min_time(self):
        return GregorianTime(10, 0)

    def get_max_time(self):
        return GregorianTime(20, 0)

    def format_period(self, period):
        return "%s to %s" % (period.start_time, period.end_time)

    def get_min_zoom_delta(self):
        return (GregorianTimeDelta(1), "Can't zoom deeper than 1")

    def now(self):
        return GregorianTime(0, 0)

    def __eq__(self, other):
        return isinstance(other, ATimeType)

    def __ne__(self, other):
        return not (self == other)


def time_period(start, end):
    return TimePeriod(GregorianTime(start, 0), GregorianTime(end, 0))
