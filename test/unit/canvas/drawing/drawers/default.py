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


from unittest.mock import Mock
import wx

from timelinelib.canvas.appearance import Appearance
from timelinelib.canvas.backgrounddrawers.defaultbgdrawer import DefaultBackgroundDrawer
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data import Event
from timelinelib.canvas.drawing.drawers.default import DefaultDrawingAlgorithm
from timelinelib.canvas.drawing.drawers import get_progress_color
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.canvas.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.cases.wxapp import WxAppTestCase
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian


IMAGE_SIZE = (500, 200)
IMAGE_WIDTH, IMAGE_HEIGHT = IMAGE_SIZE
BASELINE_Y_POS = IMAGE_HEIGHT // 2
TEXT_SIZE = (50, 10)


class describe_default_drawer(WxAppTestCase):

    def test_draws_period_event_below_baseline(self):
        self.given_event(name="vacation",
                         start=human_time_to_gregorian("1 Feb 2010"),
                         end=human_time_to_gregorian("1 Aug 2010"))
        self.when_timeline_is_drawn()
        self.assert_text_drawn_below("vacation", BASELINE_Y_POS)

    def test_draws_non_period_event_above_baseline(self):
        self.given_event(name="mike's birthday",
                         start=human_time_to_gregorian("1 Feb 2010"),
                         end=human_time_to_gregorian("1 Feb 2010"))
        self.when_timeline_is_drawn()
        self.assert_text_drawn_above("mike's birthday", BASELINE_Y_POS)

    def given_event(self, name, start, end, progress=0):
        event = Event().update(start, end, name)
        event.set_progress(progress)
        self.timeline.save_event(event)

    def when_timeline_is_drawn(self):
        appearance = Appearance()
        self.drawer.draw(self.dc, self.timeline, self.view_properties, appearance)

    def assert_text_drawn_above(self, text, y_limit):
        _, y = self.position_of_drawn_text(text)
        self.assertTrue(y < y_limit)

    def assert_text_drawn_below(self, text, y_limit):
        _, y = self.position_of_drawn_text(text)
        self.assertTrue(y > y_limit)

    def position_of_drawn_text(self, text_to_look_for):
        for ((text, x, y), _) in self.dc.DrawText.call_args_list:
            if text == text_to_look_for:
                return (x, y)
        self.fail("Text '%s' never drawn." % text_to_look_for)

    def setUp(self):
        WxAppTestCase.setUp(self)
        self.drawer = DefaultDrawingAlgorithm()
        self.drawer.set_event_box_drawer(DefaultEventBoxDrawer())
        self.drawer.set_background_drawer(DefaultBackgroundDrawer())
        self.dc = Mock(wx.DC)
        self.dc.GetSize.return_value = IMAGE_SIZE
        self.dc.GetTextExtent.return_value = TEXT_SIZE
        self.timeline = MemoryDB()
        self.view_properties = ViewProperties()
        self.view_properties.displayed_period = gregorian_period(
            "1 Jan 2010",
            "1 Jan 2011"
        )


class describe_progress_color(UnitTestCase):

    def test_progress_color(self):
        self.assertEqual(get_progress_color((255, 255, 255)), (255, 255, 255))
        self.assertEqual(get_progress_color((100, 100, 100)), (120, 120, 120))
        self.assertEqual(get_progress_color((100, 150, 200)), (50.88435374149661, 97.14285714285714, 143.40136054421765))
