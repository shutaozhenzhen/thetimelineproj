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

from timelinelib.dataimport.tutorial import GregorianTutorialTimelineCreator
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.maincanvas import MainCanvas
from timelinelib.wxgui.components.maincanvas.periodbase import SelectPeriodByDragInputHandler


class SelectperiodByDragInputHandler(UnitTestCase):

    def test_no_exception_when_julian_day_lt_0(self):
        try:
            self.simulate_drag_where_julian_day_becomes_lt_zero()
            self.when_mouse_moved()
            self.assert_(True)
        except ValueError:
            self.assert_(False)

    def when_mouse_moved(self):
        self.handler.mouse_moved(Cursor(10, 10), Keyboard())

    def simulate_drag_where_julian_day_becomes_lt_zero(self):
        canvas = Mock(MainCanvas)
        canvas.GetSize.return_value = (0, 0)
        canvas.Snap.return_value = human_time_to_gregorian("1 Dec 2013")
        canvas.GetDb.return_value = GregorianTutorialTimelineCreator().db
        canvas.GetTimeAt.return_value = human_time_to_gregorian("1 Dec 2013")
        state = Mock()
        self.handler = SelectPeriodByDragInputHandler(state, canvas, human_time_to_gregorian("1 Dec 2013"))
