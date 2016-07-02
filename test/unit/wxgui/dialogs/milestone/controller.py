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


from mock import Mock
from mock import sentinel

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.milestone.view import EditMilestoneDialog
from timelinelib.wxgui.dialogs.milestone.controller import EditMilestoneDialogController
from timelinelib.canvas.data.milestone import Milestone
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.canvas.data.timeperiod import TimePeriod
from timelinelib.canvas.data.db import MemoryDB


class describe_edit_milestone_dialog_controller(UnitTestCase):

    def test_is_initialized(self):
        self.simulate_dialog_init(self.db, self.milestone)
        self.assertEqual(GregorianTimeType(), self.controller._time_type)
        self.assertEqual(self.milestone, self.controller._milestone)
        self.view.PopulateControls.assert_called_with(self.milestone.time_period.start_time,
                                                      self.milestone.get_text(),
                                                      self.milestone.get_default_color())

    def test_can_get_time_from_view(self):
        self.view.GetTime.return_value = self.start_time
        time = self.controller.view.GetTime()
        self.assertEqual(time, self.start_time)

    def test_can_get_description_from_view(self):
        self.view.GetDescription.return_value = sentinel.DESCRIPTION
        description = self.controller.view.GetDescription()
        self.assertEqual(description, sentinel.DESCRIPTION)

    def test_can_get_colour_from_view(self):
        self.view.GetColour.return_value = sentinel.COLOUR
        colour = self.controller.view.GetColour()
        self.assertEqual(colour, sentinel.COLOUR)

    def test_milestone_updated_on_ok(self):
        time_period = TimePeriod(GregorianTimeType(), self.start_time, self.start_time)
        self.simulate_user_enters_description("Aha")
        self.simulate_user_enters_colour((127, 127, 127))
        self.simulate_user_enters_time(self.start_time)
        self.simulate_ok_clicked()
        self.milestone.set_description.assert_called_with("Aha")
        self.milestone.set_default_color.assert_called_with((127, 127, 127))
        self.milestone.set_time_period.assert_called_with(time_period)
        self.assertEqual(self.view.Close.call_count, 1)

    def simulate_user_enters_description(self, description):
        self.view.GetDescription.return_value = description

    def simulate_user_enters_colour(self, colour):
        self.view.GetColour.return_value = colour

    def simulate_user_enters_time(self, time):
        self.view.GetTime.return_value = time

    def simulate_ok_clicked(self):
        self.controller.on_ok_clicked(None)

    def simulate_dialog_init(self, time_type, milestone):
        self.controller.on_init(time_type, milestone)

    def setUp(self):
        self.db = Mock(MemoryDB)
        self.db.time_type = GregorianTimeType()
        self.start_time = human_time_to_gregorian("1 Jan 2010")
        self.milestone = Mock(Milestone)
        self.milestone.get_default_color.return_value = (0, 0, 255)
        self.milestone.get_text.return_value = ""
        self.milestone.time_period = TimePeriod(self.db.time_type, self.start_time, self.start_time)
        self.view = Mock(EditMilestoneDialog)
        self.controller = EditMilestoneDialogController(self.view)
        self.simulate_dialog_init(self.db, self.milestone)