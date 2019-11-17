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
from unittest.mock import sentinel

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.memorydb.db import MemoryDB
from timelinelib.canvas.data.milestone import Milestone
from timelinelib.canvas.data.timeperiod import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.dialogs.milestone.controller import EditMilestoneDialogController
from timelinelib.wxgui.dialogs.milestone.view import EditMilestoneDialog


class describe_edit_milestone_dialog_controller(UnitTestCase):

    def test_is_initialized(self):
        self.simulate_dialog_init(self.db, self.milestone)
        self.assertEqual(GregorianTimeType(), self.controller._time_type)
        self.assertEqual(self.milestone, self.controller._milestone)
        self.view.SetTime.assert_called_with(self.start_time)
        self.view.SetColor.assert_called_with(self.milestone.get_default_color())
        self.view.SetDescription.assert_called_with(self.milestone.get_description())
        self.view.SetCategory.assert_called_with(self.milestone.get_category())

    def test_can_get_time_from_view(self):
        self.assertEqual(self.controller.view.GetTime(), self.start_time)

    def test_can_get_description_from_view(self):
        self.assertEqual(self.controller.view.GetDescription(), sentinel.DESCRIPTION)

    def test_can_get_colour_from_view(self):
        self.view.GetColour.return_value = sentinel.COLOUR
        colour = self.controller.view.GetColour()
        self.assertEqual(colour, sentinel.COLOUR)

    def test_milestone_updated_on_ok(self):
        time_period = TimePeriod(self.start_time, self.start_time)
        self.simulate_user_enters_description("Aha")
        self.simulate_user_enters_colour((127, 127, 127))
        self.simulate_user_enters_time(self.start_time)
        self.simulate_ok_clicked()
        self.milestone.set_description.assert_called_with("Aha")
        self.milestone.set_default_color.assert_called_with((127, 127, 127))
        self.milestone.set_time_period.assert_called_with(time_period)
        self.assertEqual(self.view.Close.call_count, 1)

    def test_db_updated_on_ok(self):
        self.simulate_dialog_init(self.db, None)
        self.simulate_user_enters_description("Aha")
        self.simulate_user_enters_colour((127, 127, 127))
        self.simulate_user_enters_time(self.start_time)
        self.simulate_ok_clicked()
        self.assertEqual(self.db.save_event.call_count, 1)
        self.assertEqual(self.controller.get_milestone().get_description(), "Aha")

    def test_db_updated_when_no_description_on_ok(self):
        self.simulate_dialog_init(self.db, None)
        self.simulate_user_enters_description("")
        self.simulate_user_enters_colour((127, 127, 127))
        self.simulate_user_enters_time(self.start_time)
        self.simulate_ok_clicked()
        self.assertEqual(self.db.save_event.call_count, 1)
        self.assertEqual(self.controller.get_milestone().get_description(), None)

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
        self.milestone.get_time.return_value = self.start_time
        self.milestone.get_time_period.return_value = TimePeriod(self.start_time, self.start_time)
        self.view = self._mock_view()
        self.controller = EditMilestoneDialogController(self.view)
        self.simulate_dialog_init(self.db, self.milestone)

    def _mock_view(self):
        view = Mock(EditMilestoneDialog)
        view.GetDescription.return_value = sentinel.DESCRIPTION
        view.GetTime.return_value = self.start_time
        return view
