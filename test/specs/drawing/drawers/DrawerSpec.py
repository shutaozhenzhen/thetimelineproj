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


import wx
from mock import Mock

from timelinelib.calendar.gregorian import GregorianUtils
from timelinelib.canvas.backgrounddrawers.defaultbgdrawer import DefaultBackgroundDrawer
from timelinelib.canvas.drawing.drawers.default import DefaultDrawingAlgorithm
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.canvas.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
from timelinelib.config.dotfile import Config
from timelinelib.data.db import MemoryDB
from timelinelib.data import Event, TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.time.gregoriantime import GregorianTimeType


IMAGE_SIZE = (500, 200)
IMAGE_WIDTH, IMAGE_HEIGHT = IMAGE_SIZE
BASELINE_Y_POS = IMAGE_HEIGHT / 2
TEXT_SIZE = (50, 10)


class DrawerSpec(UnitTestCase):

    def test_draws_period_event_below_baseline(self):
        self.given_event(name="vacation",
                         start=GregorianUtils.from_date(2010, 2, 1).to_time(),
                         end=GregorianUtils.from_date(2010, 8, 1).to_time())
        self.when_timeline_is_drawn()
        self.assert_text_drawn_below("vacation", BASELINE_Y_POS)

    def test_draws_non_period_event_above_baseline(self):
        self.given_event(name="mike's birthday",
                         start=GregorianUtils.from_date(2010, 2, 1).to_time(),
                         end=GregorianUtils.from_date(2010, 2, 1).to_time())
        self.when_timeline_is_drawn()
        self.assert_text_drawn_above("mike's birthday", BASELINE_Y_POS)

    def given_event(self, name, start, end, progress=0):
        event = Event(self.timeline.get_time_type(), start, end, name)
        event.set_progress(progress)
        self.timeline.save_event(event)

    def when_timeline_is_drawn(self):
        config = Config(None)
        appearance = Mock()
        self.drawer.draw(self.dc, self.timeline, self.view_properties, config, appearance)

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
        self.app = wx.App()  # a stored app is needed to create fonts
        self.drawer = DefaultDrawingAlgorithm()
        self.drawer.set_event_box_drawer(DefaultEventBoxDrawer())
        self.drawer.set_background_drawer(DefaultBackgroundDrawer())
        self.dc = Mock(wx.DC)
        self.dc.GetSizeTuple.return_value = IMAGE_SIZE
        self.dc.GetTextExtent.return_value = TEXT_SIZE
        self.timeline = MemoryDB()
        self.view_properties = ViewProperties()
        self.view_properties.displayed_period = TimePeriod(
            GregorianTimeType(),
            GregorianUtils.from_date(2010, 1, 1).to_time(),
            GregorianUtils.from_date(2011, 1, 1).to_time())
